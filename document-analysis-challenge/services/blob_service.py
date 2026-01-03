import os
from azure.storage.blob import BlobServiceClient
import streamlit as st
from utils.Config import Config

def upload_blob(file, file_name):

    """Function to upload a file to an Azure Blob Storage"""

    print(Config.STORAGE_CONNECTION_STRING)

    try:
        blob_service_client = BlobServiceClient.from_connection_string(Config.STORAGE_CONNECTION_STRING)
        blob_client = blob_service_client.get_blob_client(container = Config.CONTAINER_NAME, blob = file_name)
        blob_client.upload_blob(file, overwrite = True)
        return blob_client.url
    except Exception as e:
        st.error(f"Error sending file to Azure Blob Storage: {e}")
        return None