from .anyType import anyType

# Simpleeval (https://github.com/danthedeckie/simpleeval)
try:
    import simpleeval

    class Evaluate_Anything_invAIder:
        @classmethod
        def INPUT_TYPES(cls):
            return {"required": {
                "python_expression": ("STRING", {"default": "((a + b) - c) / 2", "multiline": False}),},
                "optional": {
                    "a": (anyType,),
                    "b": (anyType,),
                    "c": (anyType,), },
            }

        RETURN_TYPES = (anyType,"INT", "STRING",)
        RETURN_NAMES = ("ANY","INT", "info",)
        OUTPUT_NODE = True
        FUNCTION = "node"
        CATEGORY = "👾 invAIder"

        def node(self, python_expression, a=0, b=0, c=0):
            result = simpleeval.simple_eval(python_expression, names={'a': a, 'b': b, 'c': c})

            try:
                int_result = int(result)
            except (ValueError, TypeError):
                int_result = 0

            info = f"a = {a}\nb = {b}\nc = {c}\n"
            info += f"expression: {python_expression}\n\n"
            info += f"INT: " + str(int_result)

            return (result, int_result, info,)

except ImportError:
    print("Import Error\n")