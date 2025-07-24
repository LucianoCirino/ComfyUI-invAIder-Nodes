import torch

class ReverseLatentBatch_invAIder:
    
    RETURN_TYPES = ("LATENT",)
    FUNCTION = "reverselatentbatch"
    CATEGORY = "👾 invAIder"
    DESCRIPTION = """
Reverses the order of frames in video latents.
For 4D tensors: reverses batch dimension
For 5D tensors: reverses temporal dimension
"""

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                 "latents": ("LATENT",),
        },
    } 
    
    def reverselatentbatch(self, latents):
        samples = latents["samples"]
        
        print(f"Input tensor shape: {samples.shape}")
        
        if len(samples.shape) == 4:
            # 4D tensor [B, C, H, W] - reverse batch dimension
            reversed_samples = torch.flip(samples, [0])
            print(f"Reversed 4D tensor along batch dimension")
            
        elif len(samples.shape) == 5:
            # 5D tensor [B, C, T, H, W] - reverse temporal dimension
            reversed_samples = torch.flip(samples, [2])
            print(f"Reversed 5D tensor along temporal dimension")
            
        else:
            raise ValueError(f"Unsupported tensor shape: {samples.shape}. Expected 4D or 5D tensor.")
        
        print(f"Output tensor shape: {reversed_samples.shape}")
        
        # Copy the input to preserve any additional metadata
        out_latent = latents.copy()
        out_latent["samples"] = reversed_samples
        
        # If batch_index exists, reverse it appropriately
        if "batch_index" in latents:
            if len(samples.shape) == 4:
                # For 4D, reverse the batch_index list
                out_latent["batch_index"] = list(reversed(latents["batch_index"]))
            else:
                # For 5D, batch_index typically doesn't need reversing since we're reversing time, not batches
                out_latent["batch_index"] = latents["batch_index"]
        
        return (out_latent, )