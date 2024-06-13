class Signed_Integer_invAIder:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {"value": ("INT", {"default": 0, "min": -0x8000000000000000, "max": 0x7fffffffffffffff, "step": 1}),},
        }

    RETURN_TYPES = ("INT", "INT",)
    RETURN_NAMES = ("INT", "!INT",)
    FUNCTION = "node"
    CATEGORY = "👾 invAIder"

    def node(self, value):
        return (int(value), int(not bool(value)),)