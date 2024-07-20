from . import comfy_path
from comfy_extras.nodes_images import SaveAnimatedPNG

import os
import json
from PIL import Image
import numpy as np
from PIL.PngImagePlugin import PngInfo
import folder_paths
from comfy.cli_args import args

class SaveImage:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""
        self.compress_level = 4

    @classmethod
    def INPUT_TYPES(s):
        return {"required": 
                    {"images": ("IMAGE", ),
                     "filename_prefix": ("STRING", {"default": "ComfyUI"}),
                     "prefix_as_filename": ("BOOLEAN", {"default": False}),
                     "save_path": ("STRING", {"default": ""})},
                "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
                }

    RETURN_TYPES = ()
    FUNCTION = "save_images"

    OUTPUT_NODE = True

    CATEGORY = "image"

    def save_images(self, images, filename_prefix="ComfyUI", prefix_as_filename=False, save_path="", prompt=None, extra_pnginfo=None):
        if save_path:
            self.output_dir = save_path
        
        filename_prefix += self.prefix_append
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, self.output_dir, images[0].shape[1], images[0].shape[0])
        results = list()
        for (batch_number, image) in enumerate(images):
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            metadata = None
            if not args.disable_metadata:
                metadata = PngInfo()
                if prompt is not None:
                    metadata.add_text("prompt", json.dumps(prompt))
                if extra_pnginfo is not None:
                    for x in extra_pnginfo:
                        metadata.add_text(x, json.dumps(extra_pnginfo[x]))

            if prefix_as_filename:
                file = f"{filename_prefix}.png"
            else:
                filename_with_batch_num = filename.replace("%batch_num%", str(batch_number))
                file = f"{filename_with_batch_num}_{counter:05}_.png"
            
            img.save(os.path.join(full_output_folder, file), pnginfo=metadata, compress_level=self.compress_level)
            results.append({
                "filename": file,
                "subfolder": subfolder,
                "type": self.type
            })
            counter += 1

        return { "ui": { "images": results } }

########################################################################################################################

class SaveImageIfTrue_invAIder:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "save": ("BOOLEAN", {"default": True}),
                "filename_prefix": ("STRING", {"default": ""}),
                "prefix_as_filename": ("BOOLEAN", {"default": False}),
                "save_path": ("STRING", {"default": ""})
            },
            "optional": {
                "save_path": ("STRING", {"default": ""})
            },
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO"
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "node"
    OUTPUT_NODE = True
    CATEGORY = "👾 invAIder"

    def node(self, image, save, filename_prefix, prefix_as_filename, save_path="", prompt=None, extra_pnginfo=None):
        if save:
            save_image_instance = SaveImage()
            save_image_instance.output_dir = save_path if save_path else save_image_instance.output_dir
            save_image_instance.type = "output"
            save_image_instance.prefix_append = ""
            save_image_instance.compress_level = 4
            save_image_instance.save_images(image, filename_prefix, prefix_as_filename, save_path, prompt, extra_pnginfo)

        return {}
    
########################################################################################################################

class SaveAnimatedPNGIfTrue_invAIder:
    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {"images": ("IMAGE", ),
                     "filename_prefix": ("STRING", {"default": "ComfyUI"}),
                     "fps": ("FLOAT", {"default": 6.0, "min": 0.01, "max": 1000.0, "step": 0.01}),
                     "compress_level": ("INT", {"default": 4, "min": 0, "max": 9}),
                     "save": ("BOOLEAN", {"default": True}),
                     },
                "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
                }

    RETURN_TYPES = ("IMAGE", )
    RETURN_NAMES = ("PREVIEW_IMAGE", )
    FUNCTION = "node"
    OUTPUT_NODE = True
    CATEGORY = "👾 invAIder"

    def node(self, images, fps, compress_level, save, filename_prefix="ComfyUI", prompt=None, extra_pnginfo=None):
        image = None
        if save:
           image = SaveAnimatedPNG().save_images(images, fps, compress_level, filename_prefix, prompt=None, extra_pnginfo=None)["ui"]["images"]
        return (image,)