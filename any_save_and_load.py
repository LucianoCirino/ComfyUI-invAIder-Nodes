from .anyType import anyType

variable_managers = {}

########################################################################################################################

class VariableManager:
    def __init__(self):
        self.variable = None

    def set_variable(self, value):
        self.variable = value

    def get_variable(self):
        return self.variable

    def clear_variable(self):
        self.variable = None

########################################################################################################################

class Any_Save_invAIder:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Any": (anyType,),
                "var_name": ("STRING", {"default": ""}),
            },
        }

    OUTPUT_NODE = True

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    RETURN_NAMES = ("ANY",)
    RETURN_TYPES = (anyType,)

    FUNCTION = "node"
    CATEGORY = "👾 invAIder"

    def node(self, Any, var_name):
        if var_name not in variable_managers:
            variable_managers[var_name] = VariableManager()
        variable_managers[var_name].set_variable(Any)
        return (Any,)

########################################################################################################################

class Any_Load_invAIder:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "restart": (anyType, {"default": False}),
                "default": (anyType,),
                "var_name": ("STRING", {"default": ""}),
            },
        }

    OUTPUT_NODE = True

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    RETURN_TYPES = (anyType,)
    RETURN_NAMES = ("ANY",)
    FUNCTION = "node"
    CATEGORY = "👾 invAIder"

    def node(self, restart, default, var_name):
        if bool(restart):
            return (default,)

        if var_name in variable_managers:
            variable_manager = variable_managers[var_name]
            out = variable_manager.get_variable()

            if out is not None:
                if isinstance(default, (str, bool, int, float)):
                    try:
                        out = type(default)(out)
                    except (ValueError, TypeError):
                        pass
                return (out,)
        
        return (default,)