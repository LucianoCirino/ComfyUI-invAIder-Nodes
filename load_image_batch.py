import os
import re
from .anyType import anyType
from .utils import *

def file_by_directory(directory_path,AllowedType):

    Array = []
    for root, _, items in os.walk(directory_path):
        for item in items:
            if item.lower().endswith(tuple(AllowedType)):
                Array.append(os.path.join(root, item))

    return Array     

imgType_EXT = ["jpg", "jpeg", "png"]

def numeric_sort_key(filename):
    return [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', filename)]

class LoadImageBatch_invAIder:
    def __init__(self):   
        self.counter = 0 
        self.activ_index = 0
        self.path = ""
        self.Started = False
 
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": { 
                "step_size": ("INT", {"default": 1, "min": 1, "max": 150000, "step": 1}), 
                "path": ("STRING", {"default": '', "multiline": False}),
                "start_index": ("INT", {"default": 1, "min": 1, "max": 150000, "step": 1}),
            },
            "optional": { 
                "restart": (anyType,),
            }
        }

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    RETURN_TYPES = ("IMAGE", "INT", "STRING")
    RETURN_NAMES = ("IMAGE", "Index", "Info")
    FUNCTION = "node"
    CATEGORY = "👾 invAIder"

    def node(self, step_size, path, start_index, restart=0):
        # Convert the anyType inputs to their correct modes
        restart = bool(restart)

        if not self.path == path:
            self.path = path
            self.Started = False

        if restart or not self.Started:
            self.counter = 0
            self.activ_index = start_index - 1  # Adjust for 0-based index
            self.Started = True

        fileArray = []
        if os.path.exists(path):
            fileArray = sorted([f for f in os.listdir(path) if f.lower().endswith(tuple(imgType_EXT))], key=numeric_sort_key)
            if fileArray:
                self.activ_index = self.activ_index % len(fileArray)
                image_path = os.path.join(path, fileArray[self.activ_index])
                image = Image.open(image_path)
                file_name = fileArray[self.activ_index]
                index = self.activ_index + 1
                self.activ_index = (self.activ_index + step_size) % len(fileArray)
            else:
                self.Started = False 
                info = "LoadImageBatch_invAIder - Load Batch Image: Error: Empty Directory!"
                print("----")
                print(" ")
                print("\033[91m"+info+"\033[0m")
                print(" ")
                print("----")
                return None, 0, info
        else:
            self.Started = False
            info = "LoadImageBatch_invAIder - Load Image Batch: Error: Open Directory Path Failed" 
            print("----")
            print(" ")
            print("\033[91m"+info+"\033[0m")
            print(" ")
            print("----")
            return None, 0, info
            
        info = f"Index: {index}, File Name: {file_name}"  
        return pil2tensor(image), index, info