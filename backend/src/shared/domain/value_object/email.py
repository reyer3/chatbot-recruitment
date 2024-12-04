import re
from typing import Any

from ..errors import InvalidArgumentError
from .string_value_object import StringValueObject


class Email(StringValueObject):
    """Value object for email addresses"""
    
    def __init__(self, value: str):
        self._ensure_valid_email(value)
        super().__init__(value)
    
    @staticmethod
    def _ensure_valid_email(value: str) -> None:
        if not value:
            raise InvalidArgumentError("Email cannot be empty")
        
        # RFC 5322 compliant email regex
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, value):
            raise InvalidArgumentError(f"'{value}' is not a valid email")
    
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Email):
            return False
        return self.value.lower() == other.value.lower()
    
    def __hash__(self) -> int:
        return hash(self.value.lower())
