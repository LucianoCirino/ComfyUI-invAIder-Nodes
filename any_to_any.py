from .anyType import anyType

class Any_to_Any_invAIder:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "output_type": (["original", "int", "float", "string", "bool"],),
            },
            "optional": {
                "any": (anyType,),
            }
        }

    RETURN_TYPES = (anyType,)
    RETURN_NAMES = ("ANY",)
    FUNCTION = "node"
    CATEGORY = "👾 invAIder"

    def node(self, output_type, any=None):

        default_values = {
            "int": 0,
            "float": 0.0,
            "string": "",
            "bool": False,
        }

        if output_type != "original":
            try:
                if output_type == "int":
                    output = int(any)
                elif output_type == "float":
                    output = float(any)
                elif output_type == "string":
                    output = str(any)
                elif output_type == "bool":
                    output = bool(any)
            except (ValueError, TypeError):
                # If conversion fails, return the default value for the output type
                output = default_values[output_type]
        else:
            output = any

        return (output,)