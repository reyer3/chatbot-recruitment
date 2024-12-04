from ..value_object.string_value_object import StringValueObject

class FilterValue(StringValueObject):
    def is_null(self) -> bool:
        return self.value.lower() == 'null'
        
    def to_boolean(self) -> bool:
        if self.value.lower() == 'true':
            return True
        elif self.value.lower() == 'false':
            return False
        raise ValueError(f'Value {self.value} cannot be converted to boolean')
