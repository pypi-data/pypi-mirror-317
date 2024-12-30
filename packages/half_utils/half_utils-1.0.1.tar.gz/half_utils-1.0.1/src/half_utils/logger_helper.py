from logging import getLogger, basicConfig, Handler, DEBUG
from abc import ABC, abstractmethod
from os import getcwd
from os.path import join
from sys import stdout
from typing import Callable, Optional
from enum import Enum

from loguru import logger

from .file_utils import check_directory


class LogLevel(Enum):
    TRACE = 0
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    CRITICAL = 5


class LoggerHandler(ABC):
    def __init__(self, log_level: LogLevel = LogLevel.INFO,
                 log_format: Optional[str] = None,
                 without_filter: bool = False):
        self._log_level = log_level
        self._log_format = log_format
        self._without_filter = without_filter

    @property
    def log_level(self) -> LogLevel:
        return self._log_level

    @log_level.setter
    def log_level(self, log_level: LogLevel):
        if log_level.value > self._log_level.value:
            self._log_level = log_level

    @property
    def log_format(self) -> Optional[str]:
        return self._log_format

    @log_format.setter
    def log_format(self, log_format: str) -> None:
        if self._log_format is None:
            self._log_format = log_format

    @abstractmethod
    def set_handler(self, logger_filter: Callable) -> dict:
        raise NotImplementedError


class StdoutLoggerHandler(LoggerHandler):
    def __init__(self,
                 log_level: LogLevel = LogLevel.INFO,
                 log_format: Optional[str] = None,
                 without_filter: bool = False):
        super().__init__(log_level, log_format, without_filter)

    def set_handler(self, logger_filter: Callable) -> dict:
        return {
            "sink": stdout,
            "level": self._log_level.name,
            "format": self._log_format,
            "filter": None if self._without_filter else logger_filter,
        }


class FileLoggerHandler(LoggerHandler):
    def __init__(self,
                 log_level: LogLevel = LogLevel.INFO,
                 file_path: Optional[str] = None,
                 rotation: Optional[str] = None,
                 compression: Optional[str] = None,
                 log_format: Optional[str] = None,
                 file_name: str = "output_{time}.log",
                 without_filter: bool = False) -> None:
        super().__init__(log_level, log_format, without_filter)
        self._file_path = file_path
        check_directory(join(getcwd(), self._file_path), create_if_not_exist=True)
        self._log_file_path = join(getcwd(), self._file_path, file_name)
        self._rotation = rotation
        self._compression = compression

    def set_handler(self, logger_filter: Callable) -> dict:
        return {
            "sink": self._log_file_path,
            "level": self._log_level.name,
            "format": self._log_format,
            "rotation": self._rotation,
            "compression": self._compression,
            "filter": None if self._without_filter else logger_filter,
        }


class FunctionLoggerHandler(LoggerHandler):
    def __init__(self,
                 log_level: LogLevel = LogLevel.INFO,
                 callback: Optional[Callable] = None,
                 without_filter: bool = True):
        super().__init__(log_level, None, without_filter)
        self._callback = callback

    def set_handler(self, logger_filter: Callable) -> dict:
        return {
            "sink": self._callback,
            "level": self._log_level.name,
            "format": self._log_format,
            "filter": None if self._without_filter else logger_filter,
        }


class LoggerHelper:
    _logger_filter: list[Callable[[dict], bool]] = []
    _logger_handler: list[LoggerHandler] = []

    class LogHandler(Handler):
        def emit(self, record):
            logger.log(record.levelname, record.getMessage())

    @staticmethod
    def add_log_filter(func):
        LoggerHelper._logger_filter.append(func)

    @staticmethod
    def add_log_handler(handler: LoggerHandler) -> None:
        LoggerHelper._logger_handler.append(handler)

    @staticmethod
    def log_filter(message: dict) -> bool:
        for callback in LoggerHelper._logger_filter:
            if not callback(message):
                return False
        return True

    @classmethod
    def clear(cls) -> None:
        cls._logger_handler.clear()
        cls._logger_filter.clear()

    @classmethod
    def initialize_logger(cls,
                          log_level: LogLevel = LogLevel.INFO,
                          log_format: Optional[str] = None,
                          *, integration_with_logging: bool = False) -> None:
        """
        Initialize the logger.
        :param log_level: Global logger level
        :param log_format: Override default log format
        :param integration_with_logging: Whether rewrite builtin logging module output
        :return:
        """
        log_format = log_format or ("<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</> <light-red>|</> "
                                    "<yellow>{thread:<5}</> <light-red>|</> "
                                    "<magenta>{elapsed}</> <light-red>|</> "
                                    "<level>{level:8}</> <light-red>|</> "
                                    "<cyan>{name}<light-red>:</>{function}<light-red>:</>{line}</> "
                                    "<light-red>-</> <level>{message}</>")
        handlers = []
        for handler in cls._logger_handler:
            handler.log_format = log_format
            handler.log_level = log_level
            handlers.append(handler.set_handler(LoggerHelper.log_filter))
        logger.debug(f"{cls.__name__} initialized logger with {len(handlers)} handlers")
        logger.debug(f"Change global logging level to {log_level.name}")
        logger.remove()
        logger.configure(handlers=handlers)
        if integration_with_logging:
            basicConfig(level=DEBUG if log_level.name == "TRACE" else log_level.name, handlers=[])
            getLogger().addHandler(LoggerHelper.LogHandler())
