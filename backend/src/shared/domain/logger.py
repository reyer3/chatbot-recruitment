from abc import ABC, abstractmethod
from typing import Any, Dict

class Logger(ABC):
    @abstractmethod
    def info(self, message: str, context: Dict[str, Any] = None) -> None:
        pass

    @abstractmethod
    def error(self, message: str, context: Dict[str, Any] = None) -> None:
        pass

    @abstractmethod
    def debug(self, message: str, context: Dict[str, Any] = None) -> None:
        pass

    @abstractmethod
    def warning(self, message: str, context: Dict[str, Any] = None) -> None:
        pass
