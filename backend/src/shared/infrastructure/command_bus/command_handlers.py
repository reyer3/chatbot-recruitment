from typing import Dict, Type
from ...domain.command import Command
from ...domain.command_handler import CommandHandler

class CommandHandlers:
    def __init__(self):
        self._handlers: Dict[str, Type[CommandHandler]] = {}

    def register(self, command_class: Type[Command], handler: Type[CommandHandler]) -> None:
        self._handlers[command_class.__name__] = handler

    def get(self, command: Command) -> Type[CommandHandler]:
        handler = self._handlers.get(command.__class__.__name__)
        if not handler:
            raise ValueError(f'No handler registered for command {command.__class__.__name__}')
        return handler
