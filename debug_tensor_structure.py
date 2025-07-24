import torch

class DebugTensorStructure_invAIder:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "latents": ("LATENT",),
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "execute"
    CATEGORY = "👾 invAIder"
    OUTPUT_NODE = True

    def execute(self, latents):
        print(f"\033[96m=== DETAILED LATENT ANALYSIS ===\033[0m")
        
        if 'samples' in latents:
            samples = latents['samples']
            print(f"Samples shape: {samples.shape}")
            print(f"Samples dtype: {samples.dtype}")
            print(f"Number of dimensions: {len(samples.shape)}")
            
            if len(samples.shape) == 4:
                B, C, H, W = samples.shape
                print(f"Interpreted as 4D: B={B}, C={C}, H={H}, W={W}")
                print(f"Total elements in batch dimension: {B}")
                
            elif len(samples.shape) == 5:
                B, C, T, H, W = samples.shape
                print(f"Interpreted as 5D: B={B}, C={C}, T={T}, H={H}, W={W}")
                print(f"Total frames (B*T): {B*T}")
                print(f"Frames per batch: {T}")
                
            # Check if this might be a different tensor layout
            print(f"\nPossible interpretations:")
            shape = samples.shape
            total_elements = samples.numel()
            print(f"Total tensor elements: {total_elements}")
            
            # Try different ways to interpret as frames
            for i, dim in enumerate(shape):
                print(f"  If dimension {i} (size {dim}) represents frames:")
                remaining_dims = [shape[j] for j in range(len(shape)) if j != i]
                print(f"    Frame count: {dim}")
                print(f"    Each frame shape: {remaining_dims}")
                
        # Check if there are other keys in the latent dict
        print(f"\nLatent dictionary keys: {list(latents.keys())}")
        for key, value in latents.items():
            if key != 'samples':
                print(f"  {key}: {type(value)} - {value}")
                
        # Try to figure out the actual frame count
        print(f"\n\033[93mQUESTION: You mentioned 77 frames total.\033[0m")
        print(f"Current tensor shape: {samples.shape}")
        print(f"This doesn't obviously map to 77 frames.")
        print(f"Possible explanations:")
        print(f"1. The 77 frames are split across multiple tensors/batches")
        print(f"2. The tensor represents video frames in a compressed/latent space")
        print(f"3. The frame count refers to original video frames before encoding")
        print(f"4. There's additional metadata or structure we're missing")
        
        return (None,)