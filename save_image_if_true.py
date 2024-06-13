import folder_paths
from . import comfy_path
from nodes import SaveImage
from comfy_extras.nodes_images import SaveAnimatedPNG

class SaveImageIfTrue_invAIder:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "save": ("BOOLEAN", {"default": True}),
                "filename_prefix": ("STRING", {"default": ""})
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

    def node(self, image, save, filename_prefix, prompt=None, extra_pnginfo=None):
        if save:
            save_image_instance = SaveImage()
            save_image_instance.output_dir, save_image_instance.type, save_image_instance.prefix_append, save_image_instance.compress_level = folder_paths.get_output_directory(), "output", "", 4
            save_image_instance.save_images(image, filename_prefix, prompt, extra_pnginfo)

        return {}

class SaveImageIfTrue2_invAIder:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "save": ("BOOLEAN", {"default": True}),
                "filename_prefix": ("STRING", {"default": ""}),
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

    def node(self, image, save, filename_prefix, save_path, prompt=None, extra_pnginfo=None):
        if save:
            save_image_instance = SaveImage()
            save_image_instance.output_dir, save_image_instance.type, save_image_instance.prefix_append, save_image_instance.compress_level = save_path, "output", "", 4
            save_image_instance.save_images(image, filename_prefix, prompt, extra_pnginfo)

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
           #return SaveAnimatedPNG().save_images(images, fps, compress_level, filename_prefix="ComfyUI", prompt=None, extra_pnginfo=None)
           image = SaveAnimatedPNG().save_images(images, fps, compress_level, filename_prefix, prompt=None, extra_pnginfo=None)["ui"]["images"]
        return (image,)