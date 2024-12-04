from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from .command import Command

C = TypeVar('C', bound=Command)

class CommandHandler(Generic[C], ABC):
    @abstractmethod
    async def handle(self, command: C) -> None:
        pass
