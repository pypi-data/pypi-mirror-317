from typing import Optional, Dict, Any
import logging
from pydantic import BaseModel, Field


class LoggerConfig(BaseModel):
    name: str = Field(default="app")
    level: str = Field(default="INFO")
    format: str = Field(default="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handlers: Dict[str, Dict[str, Any]] = Field(
        default={
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            }
        }
    )


class LoggerFactory:
    def __init__(self, config: LoggerConfig) -> None:
        self.config = config
        self._logger: Optional[logging.Logger] = None

    def get_logger(self) -> logging.Logger:
        if self._logger is None:
            self._logger = self._create_logger()
        return self._logger

    def _create_logger(self) -> logging.Logger:
        logger = logging.getLogger(self.config.name)
        logger.setLevel(self.config.level)

        if not logger.handlers:
            formatter = logging.Formatter(self.config.format)

            for handler_config in self.config.handlers.values():
                handler_class = eval(handler_config["class"])
                handler = handler_class()
                handler.setFormatter(formatter)
                logger.addHandler(handler)

        return logger


def create_logger(
    name: str = "app",
    level: str = "INFO",
    format: Optional[str] = None,
    handlers: Optional[Dict[str, Dict[str, Any]]] = None,
) -> logging.Logger:
    """Factory function to create a logger instance with custom configuration."""
    config = LoggerConfig(
        name=name,
        level=level,
        format=format if format is not None else LoggerConfig().format,
        handlers=handlers if handlers is not None else LoggerConfig().handlers,
    )
    factory = LoggerFactory(config)
    return factory.get_logger()


# Example usage:
# logger = create_logger(name="my_app", level="DEBUG")
# logger.info("This is an info message")
# logger.debug("This is a debug message")
