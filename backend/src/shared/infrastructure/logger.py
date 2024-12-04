import logging
from typing import Any, Dict, Optional
from ..domain.logger import Logger

class PythonLogger(Logger):
    def __init__(self, name: str = __name__):
        self._logger = logging.getLogger(name)
        self._configure_logger()

    def _configure_logger(self) -> None:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)
        self._logger.setLevel(logging.INFO)

    def _format_message(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        if context:
            return f"{message} - Context: {context}"
        return message

    def info(self, message: str, context: Dict[str, Any] = None) -> None:
        self._logger.info(self._format_message(message, context))

    def error(self, message: str, context: Dict[str, Any] = None) -> None:
        self._logger.error(self._format_message(message, context))

    def debug(self, message: str, context: Dict[str, Any] = None) -> None:
        self._logger.debug(self._format_message(message, context))

    def warning(self, message: str, context: Dict[str, Any] = None) -> None:
        self._logger.warning(self._format_message(message, context))
