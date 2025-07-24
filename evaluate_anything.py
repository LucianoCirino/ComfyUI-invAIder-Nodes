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
            # Clean input values if they're strings
            cleaned_values = {}
            for key, value in {'a': a, 'b': b, 'c': c}.items():
                # Handle string values
                if isinstance(value, str):
                    # Remove 'undefined' if it appears in the string
                    cleaned_value = value.replace('undefined', '')
                    cleaned_values[key] = cleaned_value
                else:
                    cleaned_values[key] = value
                    
            # Evaluate the expression with cleaned values
            result = simpleeval.simple_eval(python_expression, names=cleaned_values)

            # If result is a string, clean it too
            if isinstance(result, str):
                result = result.replace('undefined', '')

            try:
                int_result = int(result)
            except (ValueError, TypeError):
                int_result = 0

            info = f"a = {cleaned_values['a']}\nb = {cleaned_values['b']}\nc = {cleaned_values['c']}\n"
            info += f"expression: {python_expression}\n\n"
            info += f"INT: " + str(int_result)

            return (result, int_result, info,)

except ImportError:
    print("Import Error\n")