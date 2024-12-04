from abc import ABC, abstractmethod
from typing import Type
from .command import Command
from .command_handler import CommandHandler

class CommandBus(ABC):
    @abstractmethod
    async def dispatch(self, command: Command) -> None:
        pass

    @abstractmethod
    def register(self, command_class: Type[Command], handler: Type[CommandHandler]) -> None:
        pass
