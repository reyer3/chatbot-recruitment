from abc import ABC
from dataclasses import dataclass

@dataclass
class Response(ABC):
    """Base class for all query responses.
    Usando dataclass para una implementación más pythonica."""
    pass
