from abc import ABC
from typing import Dict, Any


class DomainError(Exception, ABC):
    """Base class for domain errors"""
    ERROR_ID: str = "domain_error"
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
    
    def to_primitives(self) -> Dict[str, Any]:
        return {
            "error_id": self.ERROR_ID,
            "message": self.message
        }


class InvalidArgumentError(DomainError):
    """Error for invalid arguments in value objects or entities"""
    ERROR_ID = "invalid_argument"
    
    def __init__(self, message: str):
        super().__init__(message)


class NotFoundError(DomainError):
    """Error for when an entity is not found"""
    ERROR_ID = "not_found"
    
    def __init__(self, message: str):
        super().__init__(message)


class AlreadyExistsError(DomainError):
    """Error for when trying to create an entity that already exists"""
    ERROR_ID = "already_exists"
    
    def __init__(self, message: str):
        super().__init__(message)


class ValidationError(DomainError):
    """Error for validation failures in domain rules"""
    ERROR_ID = "validation_error"
    
    def __init__(self, message: str):
        super().__init__(message)


class UnauthorizedError(DomainError):
    """Error for unauthorized operations"""
    ERROR_ID = "unauthorized"
    
    def __init__(self, message: str):
        super().__init__(message)


class ForbiddenError(DomainError):
    """Error for forbidden operations"""
    ERROR_ID = "forbidden"
    
    def __init__(self, message: str):
        super().__init__(message)
