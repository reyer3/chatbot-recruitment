from abc import ABC
from dataclasses import dataclass

@dataclass
class Query(ABC):
    """Base class for all queries in the system.
    En Python usamos dataclasses para tener una implementación más limpia
    de las clases de datos, equivalente a las interfaces de TS."""
    pass
