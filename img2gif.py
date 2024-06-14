import os
import re
from PIL import Image

def numeric_sort_key(filename):
    return [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', filename)]

class img2gif_invAIder:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "Image_dir": ("STRING", {"default": '', "multiline": False}),
                "output_path": ("STRING", {"default": '', "multiline": False}),
                "output_filename": ("STRING", {"default": '', "multiline": False}),
                "FPS": ("INT", {"default": 10, "min": 1, "max": 18446744073709551615, "step": 1}),
                "Loop": (["Start->END->Start", "Start->END"],),
                "Sort_Order": (["Alphabetical", "Numeric"],),
            },
            "optional": {
                "merge_folders": ("PATH",),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("Info",)
    FUNCTION = "node"  

    OUTPUT_NODE = True

    CATEGORY = "👾 invAIder"

    def node(self, Image_dir, output_path, output_filename, FPS, Loop, Sort_Order, merge_folders=None): 
        info = ""
        bilder_ordner = Image_dir if merge_folders is None else merge_folders
        frame_count = FPS

        if not os.path.isdir(bilder_ordner):
            info += f"Folder not exist: {bilder_ordner}" 
            print("img2gif_invAIder : " + info)
            return info,
    
        images = []
        empty_Image_dir = True
        filenames = os.listdir(bilder_ordner)

        if Sort_Order == "Numeric":
            filenames.sort(key=numeric_sort_key)
        else:
            filenames.sort()

        for filename in filenames:
            if filename.endswith(".jpg") or filename.endswith(".png"):
                filepath = os.path.join(bilder_ordner, filename)
                images.append(Image.open(filepath).convert("RGBA"))
                empty_Image_dir = False

        if empty_Image_dir: 
            info += f"No JPG/PNG in: {bilder_ordner}" 
            print("img2gif_invAIder : " + info)
            return info, 

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        if not output_filename:
            raise ValueError("No output filename provided.")

        # Ensure the output filename has the ".gif" extension
        output_filename = os.path.splitext(output_filename)[0] + ".gif"
        ausgabedatei = os.path.join(output_path, output_filename)

        full_image = images if Loop == "Start->END" else images + images[::-1]

        # Get the size of the first frame
        frame_size = full_image[0].size

        # Create a list to store the frames with transparent background
        frames_with_transparent_bg = []

        for frame in full_image:
            # Create a transparent background for each frame
            transparent_bg = Image.new("RGBA", frame_size, (0, 0, 0, 0))
            # Paste the frame onto the transparent background
            transparent_bg.paste(frame, (0, 0), mask=frame)
            frames_with_transparent_bg.append(transparent_bg)

        print("\n")
        frames_with_transparent_bg[0].save(ausgabedatei, save_all=True, append_images=frames_with_transparent_bg[1:], loop=0, duration=1000//frame_count, disposal=2)

        info += f"GIF : {ausgabedatei}"
        return info,