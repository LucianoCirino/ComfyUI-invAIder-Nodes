import torch
from nodes import MAX_RESOLUTION
from .utils import *
from PIL import ImageOps, ImageChops

class ImageCrop_invAIder:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "width": ("INT", {"default": 256, "min": 0, "max": MAX_RESOLUTION, "step": 8}),
                "height": ("INT", {"default": 256, "min": 0, "max": MAX_RESOLUTION, "step": 8}),
                "position": (["top-left", "top-center", "top-right", "right-center", "bottom-right", "bottom-center", "bottom-left", "left-center", "center"],),
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

    def node(self, image, width, height, position, x_offset, y_offset, mask=None):
        # Convert the image tensor to PIL Image
        pil_image = tensor2pil(image)

        # Get the dimensions of the PIL Image
        ow, oh = pil_image.size

        width = min(ow, width)
        height = min(oh, height)

        if "center" in position:
            x = round((ow - width) / 2)
            y = round((oh - height) / 2)
        if "top" in position:
            y = 0
        if "bottom" in position:
            y = oh - height
        if "left" in position:
            x = 0
        if "right" in position:
            x = ow - width

        x += x_offset
        y += y_offset

        x2 = x + width
        y2 = y + height

        if x2 > ow:
            x2 = ow
        if x < 0:
            x = 0
        if y2 > oh:
            y2 = oh
        if y < 0:
            y = 0

        '''
        # Step 1: Extract the mask from the image or use the input mask
        if pil_image.mode == "RGBA":
            mask = ImageOps.invert(pil_image.split()[-1])  # Extract the alpha channel as the mask
        else:
            if mask is not None:
                mask = tensor2pil(mask)
            else:
                mask = Image.new("L", pil_image.size, 0)  # Create a black mask (no alpha)
        '''

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

        return (output_rgb, output_mask, output_rgba, x_offset, y_offset)