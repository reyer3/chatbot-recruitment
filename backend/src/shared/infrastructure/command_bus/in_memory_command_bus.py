from typing import Type
from ...domain.command import Command
from ...domain.command_bus import CommandBus
from ...domain.command_handler import CommandHandler
from .command_handlers import CommandHandlers

class InMemoryCommandBus(CommandBus):
    def __init__(self, command_handlers: CommandHandlers):
        self._command_handlers = command_handlers

    async def dispatch(self, command: Command) -> None:
        handler_class = self._command_handlers.get(command)
        handler = handler_class()
        await handler.handle(command)

    def register(self, command_class: Type[Command], handler: Type[CommandHandler]) -> None:
        self._command_handlers.register(command_class, handler)
