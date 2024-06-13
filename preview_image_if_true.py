from . import comfy_path
from nodes import PreviewImage

class PreviewImageifTrue_invAIder:
    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {"images": ("IMAGE", ),
                     "preview": ("BOOLEAN", {"default": True})},
                "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
                }

    OUTPUT_NODE = True
    RETURN_TYPES = ()
    FUNCTION = "node"
    CATEGORY = "👾 invAIder"



    def node(self, images, preview, prompt=None, extra_pnginfo=None):
        #if preview:
            #preview_image = PreviewImage().save_images(images, prompt=prompt, extra_pnginfo=extra_pnginfo)["ui"]
        #else:
        #    preview_image = { "images": list() }
        #return { "ui": preview_image }

        def is_image_path(variable):
            if isinstance(variable, list) and len(variable) == 1:
                item = variable[0]
                if isinstance(item, dict) and 'filename' in item and 'subfolder' in item and 'type' in item:
                    return True
            return False
    
        if preview:
            if is_image_path(images):
                return { "ui": { "images": images, "animated": (True,)} }
            return PreviewImage().save_images(images, prompt=prompt, extra_pnginfo=extra_pnginfo)
        return { "images": list() }
