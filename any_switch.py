from .anyType import anyType

class Any_Switch_invAIder:

  @classmethod
  def INPUT_TYPES(cls):
    return {
      "required": {},
      "optional": {
        "any_01": (anyType,),
        "any_02": (anyType,),
      },
    }

  RETURN_TYPES = (anyType,)
  RETURN_NAMES = ("ANY",)
  FUNCTION = "node"
  CATEGORY = "👾 invAIder"

  def node(self, any_01=None, any_02=None):
    """Chooses the first non-empty item to output."""
    any_value = None
    if any_01 is not None:
      any_value = any_01
    elif any_02 is not None:
      any_value = any_02

    return (any_value,)
  
########################################################################################################################

class Any_Switch_Medium_invAIder:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "any_01": (anyType,),
                "any_02": (anyType,),
                "any_03": (anyType,),
                "any_04": (anyType,),
                "any_05": (anyType,),
            },
        }

    RETURN_TYPES = (anyType,)
    RETURN_NAMES = ("ANY",)
    FUNCTION = "node"
    CATEGORY = "👾 invAIder"

    def node(self, any_01=None, any_02=None, any_03=None, any_04=None, any_05=None):
        """Chooses the first non-empty item to output."""
        any_value = None
        if any_01 is not None:
            any_value = any_01
        elif any_02 is not None:
            any_value = any_02
        elif any_03 is not None:
            any_value = any_03
        elif any_04 is not None:
            any_value = any_04
        elif any_05 is not None:
            any_value = any_05
        return (any_value,)
    
########################################################################################################################

class Any_Switch_Large_invAIder:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "any_01": (anyType,),
                "any_02": (anyType,),
                "any_03": (anyType,),
                "any_04": (anyType,),
                "any_05": (anyType,),
                "any_06": (anyType,),
                "any_07": (anyType,),
                "any_08": (anyType,),
                "any_09": (anyType,),
                "any_10": (anyType,),
            },
        }

    RETURN_TYPES = (anyType,)
    RETURN_NAMES = ("ANY",)
    FUNCTION = "node"
    CATEGORY = "👾 invAIder"

    def node(self, any_01=None, any_02=None, any_03=None, any_04=None, any_05=None,
             any_06=None, any_07=None, any_08=None, any_09=None, any_10=None):
        """Chooses the first non-empty item to output."""
        any_value = None
        if any_01 is not None:
            any_value = any_01
        elif any_02 is not None:
            any_value = any_02
        elif any_03 is not None:
            any_value = any_03
        elif any_04 is not None:
            any_value = any_04
        elif any_05 is not None:
            any_value = any_05
        elif any_06 is not None:
            any_value = any_06
        elif any_07 is not None:
            any_value = any_07
        elif any_08 is not None:
            any_value = any_08
        elif any_09 is not None:
            any_value = any_09
        elif any_10 is not None:
            any_value = any_10
        return (any_value,)