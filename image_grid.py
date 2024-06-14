import math
import os
import glob
from PIL import Image, ImageOps
from .utils import *

ALLOWED_EXT = ('.jpeg', '.jpg', '.png',
                        '.tiff', '.gif', '.bmp', '.webp')

class ImageGrid_invAIder:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images_path": ("STRING", {"default":"./ComfyUI/input/", "multiline": False}),
                "pattern_glob": ("STRING", {"default":"*", "multiline": False}),
                "number_of_columns": ("INT", {"default":6, "min": 1, "max": 24, "step":1}),
                "max_cell_size": ("INT", {"default":256, "min":32, "max":1280, "step":1}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "create_grid_image"

    CATEGORY = "👾 invAIder"

    def create_grid_image(self, images_path, pattern_glob="*", number_of_columns=6,
                            max_cell_size=256):

        if not os.path.exists(images_path):
            print(f"The grid image path `{images_path}` does not exist!")
            return (pil2tensor(Image.new("RGBA", (512,512), (0,0,0,0))),)

        paths = glob.glob(os.path.join(images_path, pattern_glob))
        image_paths = []
        for path in paths:
            if path.lower().endswith(ALLOWED_EXT) and os.path.exists(path):
                image_paths.append(path)

        grid_image = self.smart_grid_image(image_paths, int(number_of_columns), (int(max_cell_size), int(max_cell_size)))

        return (pil2tensor(grid_image),)

    def smart_grid_image(self, images, cols=6, size=(256,256)):

        # calculate row height
        max_width, max_height = size
        row_height = 0
        images_resized = []
        for image in images:
            img = Image.open(image).convert('RGBA')

            img_w, img_h = img.size
            aspect_ratio = img_w / img_h
            if aspect_ratio > 1: # landscape
                thumb_w = min(max_width, img_w)
                thumb_h = thumb_w / aspect_ratio
            else: # portrait
                thumb_h = min(max_height, img_h)
                thumb_w = thumb_h * aspect_ratio

            # pad the image to match the maximum size and center it within the cell
            pad_w = max_width - int(thumb_w)
            pad_h = max_height - int(thumb_h)
            left = pad_w // 2
            top = pad_h // 2
            right = pad_w - left
            bottom = pad_h - top
            padding = (left, top, right, bottom)  # left, top, right, bottom
            img_resized = ImageOps.expand(img.resize((int(thumb_w), int(thumb_h))), padding)

            images_resized.append(img_resized)
            row_height = max(row_height, img_resized.size[1])
        row_height = int(row_height)

        # calculate the number of rows
        total_images = len(images_resized)
        rows = math.ceil(total_images / cols)

        # create empty image with transparent background to put thumbnails
        new_image = Image.new('RGBA', (cols*size[0], rows*row_height), (0,0,0,0))

        for i, img in enumerate(images_resized):
            x = (i % cols) * size[0]
            y = (i // cols) * row_height
            if img.size == (size[0], size[1]):
                new_image.paste(img, (x, y, x+img.size[0], y+img.size[1]))
            else:
                # Resize image to match size parameter
                img = img.resize((size[0], size[1]))
                new_image.paste(img, (x, y, x+size[0], y+size[1]))

        return new_image