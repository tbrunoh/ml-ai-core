import cv2
import numpy as np
import io


class ImageUtils:
    def __init__(self):
        pass
    def resize(imgPath:str,len:int,width:int):
        image = cv2.imread(imgPath)
        return cv2.resize(image,(len,width))