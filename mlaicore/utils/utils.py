import torch
import subprocess
import os
import re
import requests
class Utils:
    def __init__(self):
        pass
    def set_accelerator():
        device = torch.accelerator.current_accelerator().type if torch.accelerator.is_available() else "cpu"
        print(f"using {device} device")
        return device

    def create_folder(folder_path):
        """Creates a folder if it doesn't exist using subprocess."""
        if not os.path.exists(folder_path):
            subprocess.run(["mkdir", "-p", folder_path], check=True)
            print(f"Folder created: {folder_path}")
        else:
            print(f"Folder already exists: {folder_path}")

    def extract_image_filename(image_url: str, ext:str = "png"):
        match = re.search(rf"^[^-]+-(-*\d+)\.{ext}", image_url)
        return match.group(1) if match else "unknown"
    
    def validate_url(url: str):
        invalid_urls = []
        try:
            # Send a HEAD request to check the URL
            response = requests.head(url, timeout=5)
            if response.status_code == 200:
                pass  # URL is valid
            else:
                invalid_urls.append(url)
        except requests.RequestException:
            invalid_urls.append(url)
        
        return invalid_urls