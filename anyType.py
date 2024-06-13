# Hack: string type that is always equal in not equal comparisons
class AnyType_fill(str):
    def __ne__(self, __value: object) -> bool:
        return False
    
anyType = AnyType_fill("*")