import torch

class WanLatentConcat_invAIder:
    """
    ComfyUI node for concatenating video latent tensors along the temporal dimension.
    Combines multiple latent sequences into a single longer sequence.
    """
    
    RETURN_TYPES = ("LATENT",)
    FUNCTION = "concat_latents"
    CATEGORY = "👾 invAIder"
    DESCRIPTION = """
Concatenates latent tensors along the temporal dimension.
Input latents are combined in order to create a longer sequence.
All inputs must have the same batch size, channels, height, and width.
"""

    @classmethod
    def INPUT_TYPES(s):
        return {
            "optional": {
                "latent1": ("LATENT",),
                "latent2": ("LATENT",),
                "latent3": ("LATENT",),
            },
        }

    def concat_latents(self, latent1=None, latent2=None, latent3=None):
        # Collect all provided latents
        latents_to_concat = []
        
        for i, latent in enumerate([latent1, latent2, latent3], 1):
            if latent is not None:
                latents_to_concat.append(latent)
        
        # Check if we have at least one latent
        if len(latents_to_concat) == 0:
            raise ValueError("At least one latent input must be provided")
        
        # If only one latent, return it as-is
        if len(latents_to_concat) == 1:
            print("Only one latent provided, returning as-is")
            return (latents_to_concat[0],)
        
        # Extract samples from each latent
        samples_list = []
        total_frames = 0
        
        for i, latent in enumerate(latents_to_concat):
            samples = latent["samples"]
            samples_list.append(samples)
            
            # Get frame count based on tensor dimensions
            if len(samples.shape) == 5:
                # 5D tensor: [B, C, T, H, W]
                frame_count = samples.shape[2]
            elif len(samples.shape) == 4:
                # 4D tensor: [B, C, H, W] - treat as single frame
                frame_count = samples.shape[0]
            else:
                raise ValueError(f"Unsupported tensor shape: {samples.shape}")
            
            total_frames += frame_count
            print(f"Latent {i+1}: {list(samples.shape)} - {frame_count} frames")
        
        # Validate that all tensors have compatible shapes
        first_samples = samples_list[0]
        for i, samples in enumerate(samples_list[1:], 1):
            if len(samples.shape) != len(first_samples.shape):
                raise ValueError(f"All latents must have the same number of dimensions. "
                               f"Latent 1: {len(first_samples.shape)}D, Latent {i+1}: {len(samples.shape)}D")
            
            if len(samples.shape) == 5:
                # Check B, C, H, W dimensions match (T can differ)
                if (samples.shape[0] != first_samples.shape[0] or  # Batch
                    samples.shape[1] != first_samples.shape[1] or  # Channels
                    samples.shape[3] != first_samples.shape[3] or  # Height
                    samples.shape[4] != first_samples.shape[4]):   # Width
                    raise ValueError(f"Incompatible shapes. Latent 1: {list(first_samples.shape)}, "
                                   f"Latent {i+1}: {list(samples.shape)}. "
                                   f"Batch, channels, height, and width must match.")
            elif len(samples.shape) == 4:
                # Check C, H, W dimensions match (B can differ)
                if (samples.shape[1] != first_samples.shape[1] or  # Channels
                    samples.shape[2] != first_samples.shape[2] or  # Height
                    samples.shape[3] != first_samples.shape[3]):   # Width
                    raise ValueError(f"Incompatible shapes. Latent 1: {list(first_samples.shape)}, "
                                   f"Latent {i+1}: {list(samples.shape)}. "
                                   f"Channels, height, and width must match.")
        
        # Concatenate tensors
        if len(first_samples.shape) == 5:
            # 5D tensors: concatenate along temporal dimension (dim=2)
            concatenated_samples = torch.cat(samples_list, dim=2)
            print(f"Concatenated 5D tensors along temporal dimension")
        elif len(first_samples.shape) == 4:
            # 4D tensors: concatenate along batch dimension (dim=0)
            concatenated_samples = torch.cat(samples_list, dim=0)
            print(f"Concatenated 4D tensors along batch dimension")
        
        print(f"Final shape: {list(concatenated_samples.shape)} - {total_frames} total frames")
        
        # Create output latent dictionary
        output_latent = {"samples": concatenated_samples.contiguous()}
        
        # Copy any additional keys from the first latent
        for key, value in latents_to_concat[0].items():
            if key != "samples":
                output_latent[key] = value
        
        return (output_latent,)