import torch
import numpy as np
from PIL import Image, ImageOps

from .utils import *

import comfy.utils
from nodes import MAX_RESOLUTION

class ImageOverlay_invAIder:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "base_image": ("IMAGE",),
                "width": ("INT", {"default": 512, "min": 0, "max": MAX_RESOLUTION, "step": 1}),
                "height": ("INT", {"default": 512, "min": 0, "max": MAX_RESOLUTION, "step": 1}),
                "x_offset": ("INT", {"default": 0, "min": -48000, "max": 48000, "step": 10}),
                "y_offset": ("INT", {"default": 0, "min": -48000, "max": 48000, "step": 10}),
                "rotation": ("INT", {"default": 0, "min": -180, "max": 180, "step": 5}),
                "opacity": ("FLOAT", {"default": 0, "min": 0, "max": 100, "step": 5}),
            },
            "optional": {
                "overlay_image": ("IMAGE",),
                "base_mask": ("MASK",),
                "overlay_mask": ("MASK",),
                "overlay_resize": (["None", "Fit", "Resize by rescale_factor", "Resize to width & heigth"],),
                "resize_method": (["nearest-exact", "bilinear", "area"],),
                "rescale_factor": ("FLOAT", {"default": 1, "min": 0.01, "max": 16.0, "step": 0.1}),
            }
        }

    RETURN_TYPES = ("IMAGE", "IMAGE", "MASK")
    RETURN_NAMES = ("RGB_IMAGE", "RGBA_IMAGE", "MASK")
    FUNCTION = "node"
    CATEGORY = "👾 invAIder"

    def node(self, base_image, width, height, x_offset, y_offset, rotation, opacity,
             overlay_image=None, base_mask=None, overlay_mask=None, overlay_resize=None,
             resize_method=None, rescale_factor=None):
        
        # Pack tuples and assign variables
        size = width, height
        location = x_offset, y_offset

        # Convert base image to PIL Image
        base_pil_image = tensor2pil(base_image)

        # Extract base image mask
        if base_pil_image.mode == "RGBA":
            base_mask = base_pil_image.split()[-1]  # Extract the alpha channel as the mask
        else:
            if base_mask is not None:
                base_mask = tensor2pil(base_mask)
            else:
                base_mask = Image.new("L", base_pil_image.size, 255)  # Create a white mask (no alpha)

        # Process overlay image if provided
        if overlay_image is not None:
            # Convert overlay image to PIL Image
            overlay_pil_image = tensor2pil(overlay_image)

            # Extract overlay image mask
            if overlay_pil_image.mode == "RGBA":
                overlay_mask = overlay_pil_image.split()[-1]  # Extract the alpha channel as the mask
            else:
                if overlay_mask is not None:
                    overlay_mask = tensor2pil(overlay_mask)
                else:
                    overlay_mask = Image.new("L", overlay_pil_image.size, 255)  # Create a white mask (no alpha)

            # Resize overlay image if needed
            if overlay_resize is not None:
                overlay_image_size = overlay_pil_image.size
                if overlay_resize == "Fit":
                    h_ratio = base_pil_image.size[1] / overlay_image_size[1]
                    w_ratio = base_pil_image.size[0] / overlay_image_size[0]
                    ratio = min(h_ratio, w_ratio)
                    overlay_image_size = tuple(round(dimension * ratio) for dimension in overlay_image_size)
                elif overlay_resize == "Resize by rescale_factor":
                    overlay_image_size = tuple(int(dimension * rescale_factor) for dimension in overlay_image_size)
                elif overlay_resize == "Resize to width & heigth":
                    overlay_image_size = (size[0], size[1])

                samples = overlay_image.movedim(-1, 1)
                overlay_image = comfy.utils.common_upscale(samples, overlay_image_size[0], overlay_image_size[1], resize_method, False)
                overlay_image = overlay_image.movedim(1, -1)
                overlay_pil_image = tensor2pil(overlay_image)
                overlay_mask = overlay_mask.resize(overlay_pil_image.size)

            # Rotate the overlay image and mask
            overlay_pil_image = overlay_pil_image.rotate(rotation, expand=True)
            overlay_mask = overlay_mask.rotate(rotation, expand=True)

            # Apply opacity to the overlay image
            r, g, b, a = overlay_pil_image.split()
            a = a.point(lambda x: max(0, int(x * (opacity / 100))))
            overlay_pil_image = Image.merge("RGBA", (r, g, b, a))

            # Apply the overlay image to the base image
            base_pil_image.paste(overlay_pil_image, location, mask=ImageOps.invert(overlay_mask))

        # Create the RGB and RGBA outputs
        rgb_image = base_pil_image.convert("RGB")
        rgba_image = base_pil_image.copy()
        rgba_image.putalpha(ImageOps.invert(base_mask))  # Invert the base mask and apply it as the alpha channel

        # Convert the images and mask back to tensors
        output_rgb = pil2tensor(rgb_image)
        output_rgba = pil2tensor(rgba_image)
        output_mask = pil2tensor(base_mask)

        # Return the edited base image (RGB and RGBA) and the mask
        return (output_rgb, output_rgba, output_mask)