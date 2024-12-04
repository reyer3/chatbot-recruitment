from typing import Any
from urllib.parse import urlparse

from ..errors import InvalidArgumentError
from .string_value_object import StringValueObject


class URL(StringValueObject):
    """Value object for URLs"""
    
    ALLOWED_SCHEMES = {'http', 'https'}
    
    def __init__(self, value: str):
        self._ensure_valid_url(value)
        super().__init__(value)
    
    @classmethod
    def _ensure_valid_url(cls, value: str) -> None:
        if not value:
            raise InvalidArgumentError("URL cannot be empty")
        
        try:
            parsed = urlparse(value)
            
            # Check scheme
            if parsed.scheme not in cls.ALLOWED_SCHEMES:
                raise InvalidArgumentError(f"URL scheme must be one of: {', '.join(cls.ALLOWED_SCHEMES)}")
            
            # Check netloc (domain)
            if not parsed.netloc:
                raise InvalidArgumentError("URL must contain a valid domain")
            
            # Basic domain validation
            if not all(part.isalnum() or part in '-.' for part in parsed.netloc.split('.')):
                raise InvalidArgumentError("URL contains invalid domain characters")
            
            # Must have at least one dot in domain (e.g., example.com)
            if '.' not in parsed.netloc:
                raise InvalidArgumentError("URL must contain a valid domain with TLD")
            
        except Exception as e:
            raise InvalidArgumentError(f"Invalid URL format: {str(e)}")
    
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, URL):
            return False
        # Normalize URLs for comparison
        return urlparse(self.value).geturl() == urlparse(other.value).geturl()
    
    def __hash__(self) -> int:
        return hash(urlparse(self.value).geturl())
