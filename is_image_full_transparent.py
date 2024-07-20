import torch
from PIL import Image
from .utils import *

class IsImageFullyTransparent_invAIder:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("BOOLEAN","BOOLEAN",)
    RETURN_NAMES = ("BOOLEAN","!BOOLEAN",)
    FUNCTION = "check_full_transparency"
    CATEGORY = "👾 invAIder"

    def check_full_transparency(self, image):
        # Convert the image tensor to PIL Image using the provided function
        pil_image = tensor2pil(image)
        
        # Check if the image has an alpha channel
        if pil_image.mode == 'RGBA':
            # Extract the alpha channel
            alpha = pil_image.split()[-1]

            # Check if the alpha channel is completely black (fully transparent)
            result = not alpha.getbbox()

            return (result, not result,)
        else:
            # For any image without an alpha channel, return False
            return (False,True,)