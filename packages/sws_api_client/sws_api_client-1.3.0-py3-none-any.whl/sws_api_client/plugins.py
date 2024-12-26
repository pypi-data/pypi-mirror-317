import os
import urllib.parse
import zipfile
from pydantic import BaseModel
import requests
from sws_api_client.sws_api_client import SwsApiClient
from typing import Optional, Union
import logging

logger = logging.getLogger(__name__)

class ParameterUploadUrlResponse(BaseModel):
    url: str
    key: str

class Plugins:

    def __init__(self, sws_client: SwsApiClient, endpoint: str = 'plugin_api') -> None:
        self.sws_client = sws_client
        self.endpoint = endpoint

    def get_parameter_upload_url(self, plugin_id: int, file_name:str, last_modified:int) -> ParameterUploadUrlResponse:
        url = f"/legacyPlugin/{plugin_id}/parametersUploadUrl?filename={file_name}&lastModified={last_modified}"
        response = self.sws_client.discoverable.get(self.endpoint, url)
        return ParameterUploadUrlResponse(**response)
    
    def get_parameter_from_file(self, plugin_id: int, file_path: str) -> str:
        # get file last modified date
        last_modified = os.path.getmtime(file_path)
        # get the upload URL
        upload_url = self.get_parameter_upload_url(plugin_id, os.path.basename(file_path), int(last_modified))
        # upload the file
        with open(file_path, 'rb') as file:
            requests.put(upload_url.url, data=file)
            return f"s3PluginParameterFile:{upload_url.key}"
    
    def get_parameter_file(self, key: str, download_path: Union[str, None] = None) -> Optional[object]:
        url = f"/legacyPlugin/parameterDownloadUrl?key={urllib.parse.quote(key)}"
        response = self.sws_client.discoverable.get(self.endpoint, url)
        logger.debug(f"Response: {response}")
        if response:
            # Extract the filename from the URL
            response_url = response.get('url')
            filename = urllib.parse.unquote(os.path.basename(urllib.parse.urlparse(response_url).path))
            
            # If download_path is a folder, construct the full path
            if download_path and os.path.isdir(download_path):
                download_path = os.path.join(download_path, filename)
            elif not download_path:
                # If download_path is not provided, use the current directory
                download_path = os.path.join(os.getcwd(), filename)
            
            # Ensure the directory exists
            directory = os.path.dirname(download_path)
            if not os.path.exists(directory):
                os.makedirs(directory)
            
            # Download the file from response URL
            s3_response = requests.get(response_url, stream=True)
            if s3_response.status_code == 200:
                with open(download_path, 'wb') as file:
                    for chunk in s3_response.iter_content(chunk_size=8192):
                        file.write(chunk)
                
                # Return the file handler
                return download_path
            else:
                logger.error(f"Failed to download file: HTTP {s3_response.status_code}")
                return None
        else:
            logger.error("Failed to get the download URL.")
            return None
    
    def get_all_plugins(self):
        url = f"/admin/plugin"
        response = self.sws_client.discoverable.get('is_api', url)
        return response
    
    def download_plugin_source_code(self, plugin_id: int, download_path: str) -> Optional[str]:
        """
        Downloads and extracts the plugin source code zip file to the specified location.
        
        Args:
            plugin_id (int): The ID of the plugin.
            download_path (str): The location where the zip file will be saved and extracted.
        
        Returns:
            Optional[str]: The path to the extracted folder, or None if the operation fails.
        """
        url = f"/legacyPlugin/{plugin_id}/script"
        
        # Make the API call to directly get the zip file
        response = self.sws_client.discoverable.get(self.endpoint, url, headers={"Accept": "application/zip"}, options={"raw_response":True}, stream=True)
        
        # Ensure the download_path directory exists
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        
        # Define the temporary zip file path
        zip_file_path = os.path.join(download_path, f"plugin_{plugin_id}.zip")
        
        # Save the response content as a zip file
        with open(zip_file_path, 'wb') as zip_file:
            for chunk in response.iter_content(chunk_size=8192):
                zip_file.write(chunk)
        
        # Extract the contents of the zip file
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(download_path)
        
        # Remove the temporary zip file
        os.remove(zip_file_path)
        
        logger.info(f"Plugin source code extracted to: {download_path}")
        return download_path
