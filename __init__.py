from .any_save_and_load import Any_Save_invAIder, Any_Load_invAIder
from .signed_integer import Signed_Integer_invAIder
from .number_counter import Number_Counter_invAIder
from .save_image_if_true import SaveImageIfTrue_invAIder, SaveAnimatedPNGIfTrue_invAIder
from .seed_controller import SeedControl_invAIder
from .evaluate_anything import Evaluate_Anything_invAIder
from .any_to_any import Any_to_Any_invAIder
from .int_to_bits import Integer_to_Bits_invAIder
from .any_switch import Any_Switch_invAIder, Any_Switch_Medium_invAIder, Any_Switch_Large_invAIder
from .preview_image_if_true import PreviewImageifTrue_invAIder
from .image_overlay import ImageOverlay_invAIder
from .load_image_batch import LoadImageBatch_invAIder
from .img2gif import img2gif_invAIder
from .image_grid import ImageGrid_invAIder
from .image_crop import ImageCrop_invAIder
from .is_image_full_transparent import IsImageFullyTransparent_invAIder
from .reverse_latents_batch import ReverseLatentBatch_invAIder
from .wan_latent_concat import WanLatentConcat_invAIder
from .debug_tensor_structure import DebugTensorStructure_invAIder

# A dictionary that contains all nodes you want to export with their names
NODE_CLASS_MAPPINGS = {
    "👾 Save Any": Any_Save_invAIder,
    "👾 Load Any": Any_Load_invAIder,
    "👾 Signed Integer": Signed_Integer_invAIder,
    "👾 Number Counter": Number_Counter_invAIder,
    "👾 Save Image If True": SaveImageIfTrue_invAIder,
    "👾 Save AnimPNG If True": SaveAnimatedPNGIfTrue_invAIder,
    "👾 Seed Controller": SeedControl_invAIder,
    "👾 Evaluate Anything": Evaluate_Anything_invAIder,
    "👾 Any to Any": Any_to_Any_invAIder,   
    "👾 Int to Bits": Integer_to_Bits_invAIder,
    "👾 Any Switch": Any_Switch_invAIder,
    "👾 Any Switch Medium": Any_Switch_Medium_invAIder,
    "👾 Any Switch Large": Any_Switch_Large_invAIder,
    "👾 Preview Image if True": PreviewImageifTrue_invAIder,
    "👾 Image Overlay": ImageOverlay_invAIder,
    "👾 Load Image Batch": LoadImageBatch_invAIder,
    "👾 Img to Gif": img2gif_invAIder,
    "👾 Image Grid": ImageGrid_invAIder,
    "👾 Image Crop": ImageCrop_invAIder,
    "👾 Is Image Fully Transparent": IsImageFullyTransparent_invAIder,
    "👾 Reverse Latent Batch": ReverseLatentBatch_invAIder,
    "👾 Wan Latent Concat": WanLatentConcat_invAIder,
    "👾 Debug Tensor Structure ": DebugTensorStructure_invAIder
}

__all__ = ['NODE_CLASS_MAPPINGS']