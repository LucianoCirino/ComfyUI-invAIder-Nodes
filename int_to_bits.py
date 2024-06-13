from .anyType import anyType

class Integer_to_Bits_invAIder:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "value": ("INT", {"default": 0, "min": 0, "max": 0xf, "step": 1}),
            },
        }

    RETURN_TYPES = (anyType, anyType, anyType, anyType, "STRING")
    RETURN_NAMES = ("BIT0", "BIT1", "BIT2", "BIT3", "info")
    FUNCTION = "node"
    CATEGORY = "👾 invAIder"

    def node(self, value):
        bit0 = (value & 0b00000001) != 0
        bit1 = (value & 0b00000010) != 0
        bit2 = (value & 0b00000100) != 0
        bit3 = (value & 0b00001000) != 0

        info = f"Bit Values:\n"
        info += f"  BIT0: {1 if bit0 else 0}\n"
        info += f"  BIT1: {1 if bit1 else 0}\n"
        info += f"  BIT2: {1 if bit2 else 0}\n"
        info += f"  BIT3: {1 if bit3 else 0}\n"

        return (bit0, bit1, bit2, bit3, info)
'''  
class Integer_to_Bits_invAIder:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "value": ("INT", {"default": 0, "min": 0, "max": 0xf, "step": 1}),
            },
        }

    RETURN_TYPES = ("BOOL", "BOOL", "BOOL", "BOOL", "BOOL", "BOOL", "BOOL", "BOOL")
    RETURN_NAMES = ("BIT0", "BIT1", "BIT2", "BIT3", "BIT4", "BIT5", "BIT6", "BIT7")
    FUNCTION = "node"
    CATEGORY = "👾 invAIder"

    def node(self, value):
        bit0 = (value & 0b00000001) != 0
        bit1 = (value & 0b00000010) != 0
        bit2 = (value & 0b00000100) != 0
        bit3 = (value & 0b00001000) != 0
        bit4 = (value & 0b00010000) != 0
        bit5 = (value & 0b00100000) != 0
        bit6 = (value & 0b01000000) != 0
        bit7 = (value & 0b10000000) != 0

        return (bit0, bit1, bit2, bit3, bit4, bit5, bit6, bit7,)
'''