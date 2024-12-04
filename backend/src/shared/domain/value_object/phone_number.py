import re
from typing import Any

from ..errors import InvalidArgumentError
from .string_value_object import StringValueObject


class PhoneNumber(StringValueObject):
    """Value object for phone numbers in E.164 format"""
    
    def __init__(self, value: str):
        self._ensure_valid_phone(value)
        # Store normalized format
        normalized = self._normalize_phone(value)
        super().__init__(normalized)
    
    @staticmethod
    def _normalize_phone(value: str) -> str:
        """Remove all non-digit characters except leading +"""
        return '+' + ''.join(filter(str.isdigit, value)) if value.startswith('+') else ''.join(filter(str.isdigit, value))
    
    @staticmethod
    def _ensure_valid_phone(value: str) -> None:
        if not value:
            raise InvalidArgumentError("Phone number cannot be empty")
        
        # Remove all non-digit characters except leading +
        normalized = '+' + ''.join(filter(str.isdigit, value)) if value.startswith('+') else ''.join(filter(str.isdigit, value))
        
        # Basic validation: length between 8 and 15 digits (ITU-T E.164)
        if not 8 <= len(normalized.replace('+', '')) <= 15:
            raise InvalidArgumentError(f"'{value}' is not a valid phone number length")
        
        # Check if contains only digits (and optionally leading +)
        if not re.match(r'^\+?\d+$', normalized):
            raise InvalidArgumentError(f"'{value}' contains invalid characters")
    
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, PhoneNumber):
            return False
        return self._normalize_phone(self.value) == self._normalize_phone(other.value)
    
    def __hash__(self) -> int:
        return hash(self._normalize_phone(self.value))
