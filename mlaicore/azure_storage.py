import os

from dotenv import load_dotenv
import os
import uuid
from azure.storage.blob import BlobServiceClient

load_dotenv()

AZURE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = os.getenv("AZURE_CONTAINER_NAME")

# Initialize the BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)

# Ensure the container exists (create if not)
try:
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)
    container_client.get_container_properties()
except Exception:
    container_client = blob_service_client.create_container(CONTAINER_NAME)
    

def getBlobName(filename: str, prefix: str, useFilename:bool=False) -> dict:
    ext = os.path.splitext(filename)[1]
    if useFilename:
        unique_filename = filename.replace(" ", "").lower()
    else:
        unique_filename = f"{uuid.uuid4()}{ext}"
    
    # unique_filename = f"{uuid.uuid4()}{ext}"
    blob_name = f"{prefix}/{unique_filename}"
    
    result = {
        "filename": unique_filename,
        "blob_name": blob_name
    }
    return result


async def uploadImage( filename:str, blob_name:str,file_data: bytes) -> str:
    try:
        await uploadToBucket(file_data, blob_name)
    except Exception as e:
        raise ValueError(f"Failed to upload image: {str(e)}")

    return filename

async def uploadToBucket(data:bytes|str, blob_name:str):
    try:
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=blob_name)
        blob_client.upload_blob(data, overwrite=True)
    except Exception as e:
        raise ValueError(f"Failed to upload to bucket: {str(e)}")

