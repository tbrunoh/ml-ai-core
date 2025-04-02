import pandas as pd
from PIL import Image
from torch.utils.data import Dataset
from urllib.request import urlopen


class BaseDataset(Dataset):
    def __init__(self, transform=None):
        super().__init__()
        self.transform = transform
        
    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        raise NotImplementedError("Subclasses must implement forward method")
    
    def load_image(addr:any)->Image:
        if addr.startswith("http://") or addr.startswith("https://"):
            with urlopen(addr) as response:
                image = Image.open(response).convert("RGB")
        else:
            image = Image.open(addr).convert("RGB")
            
        return image

        
        