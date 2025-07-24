import torch
from nodes import MAX_RESOLUTION
from .utils import *
from PIL import ImageOps, ImageChops, Image
import numpy as np

class ImageCrop_invAIder:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "width": ("INT", {"default": 256, "min": 0, "max": MAX_RESOLUTION, "step": 8}),
                "height": ("INT", {"default": 256, "min": 0, "max": MAX_RESOLUTION, "step": 8}),
                "position": (["top-left", "top-center", "top-right", "right-center", "bottom-right", "bottom-center", "bottom-left", "left-center", "center", "center-auto", "center-auto(left)", "center-auto(right)", "center-auto(top)", "center-auto(bottom)", "bottom-center-auto"],),
                "x_offset": ("INT", {"default": 0, "min": -99999, "step": 1}),
                "y_offset": ("INT", {"default": 0, "min": -99999, "step": 1}),
            },
            "optional": {
                "mask": ("MASK",),
            }
        }

    RETURN_TYPES = ("IMAGE", "MASK", "IMAGE", "INT", "INT")
    RETURN_NAMES = ("RGB_IMAGE", "MASK", "RGBA_IMAGE", "X_OFFSET", "Y_OFFSET")
    FUNCTION = "node"
    CATEGORY = "👾 invAIder"

    def find_content_bbox(self, image):
        if image.mode == 'RGBA':
            alpha = np.array(image.split()[-1])
            rows = np.any(alpha, axis=1)
            cols = np.any(alpha, axis=0)
        else:
            gray = np.array(image.convert('L'))
            rows = np.any(gray < 255, axis=1)
            cols = np.any(gray < 255, axis=0)
        
        rmin, rmax = np.where(rows)[0][[0, -1]] if np.any(rows) else (0, image.height - 1)
        cmin, cmax = np.where(cols)[0][[0, -1]] if np.any(cols) else (0, image.width - 1)
        
        return cmin, rmin, cmax, rmax

    def get_center_auto_crop(self, image, width, height, position, x_offset=0, y_offset=0):
        ow, oh = image.size
        cmin, rmin, cmax, rmax = self.find_content_bbox(image)
        
        # Calculate the center of the content
        content_center_x = (cmin + cmax) // 2
        content_center_y = (rmin + rmax) // 2
        
        # Calculate the crop position to center around the content
        x = content_center_x - width // 2
        y = content_center_y - height // 2
        
        # Apply offsets
        x += x_offset
        y += y_offset
        
        # Ensure the crop stays within the image bounds
        x = max(0, min(x, ow - width))
        y = max(0, min(y, oh - height))
        
        return x, y

    def node(self, image, width, height, position, x_offset, y_offset, mask=None):
        # Convert the image tensor to PIL Image
        pil_image = tensor2pil(image)

        # Get the dimensions of the PIL Image
        ow, oh = pil_image.size
        width = min(ow, width)
        height = min(oh, height)

        # Handle auto positions
        if position.startswith("center-auto") or position == "bottom-center-auto":
            x, y = self.get_center_auto_crop(pil_image, width, height, position, x_offset, y_offset)
        elif position == "center":
            x = round((ow - width) / 2) + x_offset
            y = round((oh - height) / 2) + y_offset
        elif position == "top-left":
            x, y = x_offset, y_offset
        elif position == "top-center":
            x = round((ow - width) / 2) + x_offset
            y = y_offset
        elif position == "top-right":
            x = ow - width + x_offset
            y = y_offset
        elif position == "left-center":
            x = x_offset
            y = round((oh - height) / 2) + y_offset
        elif position == "right-center":
            x = ow - width + x_offset
            y = round((oh - height) / 2) + y_offset
        elif position == "bottom-left":
            x, y = x_offset, oh - height + y_offset
        elif position == "bottom-center":
            x = round((ow - width) / 2) + x_offset
            y = oh - height + y_offset
        elif position == "bottom-right":
            x, y = ow - width + x_offset, oh - height + y_offset

        # Ensure the crop stays within the image bounds
        x = max(0, min(x, ow - width))
        y = max(0, min(y, oh - height))

        # Calculate the actual offset applied after boundary adjustment
        actual_x_offset = x - (round((ow - width) / 2) if "center" in position else (0 if "left" in position else ow - width))
        actual_y_offset = y - (round((oh - height) / 2) if "center" in position else (0 if "top" in position else oh - height))

        x2 = x + width
        y2 = y + height

        # Step 1: Extract the mask from the image or use the input mask
        if pil_image.mode == "RGBA":
            alpha_mask = ImageOps.invert(pil_image.split()[-1])  # Extract the alpha channel as the mask
            if mask is not None:
                input_mask = tensor2pil(mask)  # Convert input mask tensor to PIL image
                mask = ImageOps.invert(ImageChops.add(ImageOps.invert(input_mask), ImageOps.invert(alpha_mask)))  # Add the extracted alpha mask to the input mask
            else:
                mask = alpha_mask
        else:
            if mask is not None:
                mask = tensor2pil(mask)
            else:
                mask = Image.new("L", pil_image.size, 0)  # Create a black mask (no alpha)
    
        # Step 2: Crop both the image and the mask according to inputs
        cropped_image = pil_image.crop((x, y, x2, y2))
        cropped_mask = mask.crop((x, y, x2, y2))

        # Step 3: Create the RGB and RGBA outputs
        rgb_image = cropped_image.convert("RGB")
        rgba_image = rgb_image.copy()
        rgba_image.putalpha(ImageOps.invert(cropped_mask))  # Invert the cropped mask and apply it as the alpha channel

        # Step 4: Output the RGB image, mask, and RGBA image
        output_rgb = pil2tensor(rgb_image)
        output_mask = pil2tensor(cropped_mask)
        output_rgba = pil2tensor(rgba_image)

        return (output_rgb, output_mask, output_rgba, actual_x_offset, actual_y_offset)