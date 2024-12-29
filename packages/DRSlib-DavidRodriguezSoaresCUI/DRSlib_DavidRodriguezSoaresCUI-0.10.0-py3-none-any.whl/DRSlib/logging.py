import logging
from typing import Self


LOG_FORMAT_VERBOSE = "[%(levelname)s:%(filename)s:%(lineno)d] %(message)s"
LOG_FORMAT_EXTENDED = "[%(levelname)s:%(funcName)s] %(message)s"
LOG_FORMAT_BASIC = "[%(levelname)s] %(message)s"


def remove_handlers(logger: logging.Logger) -> logging.Logger:
    """Removes handlers from logger"""
    for h in logger.handlers:
        logger.removeHandler(h)
    return logger


class LoggerBuilder:
    """Builds your logger easily"""

    def __init__(self, name: str) -> None:
        # Get logger by name and remove parent and all handlers
        self.logger = remove_handlers(logging.getLogger(name))
        self.logger.parent = None

    def add_handler(
        self,
        handler: type,
        log_format: str = LOG_FORMAT_BASIC,
        log_level: int = logging.DEBUG,
        **kwargs
    ) -> Self:
        """Add handler to logger"""
        if log_level < self.logger.getEffectiveLevel():
            self.logger.setLevel(log_level)
        _handler: logging.Handler = handler(**kwargs)
        _handler.setFormatter(logging.Formatter(log_format))
        _handler.setLevel(log_level)
        self.logger.addHandler(_handler)
        return self

    def add_stream_handler(
        self,
        log_format: str = LOG_FORMAT_BASIC,
        log_level: int = logging.DEBUG,
        **kwargs
    ) -> Self:
        """Add handler that writes to stderr"""
        return self.add_handler(logging.StreamHandler, log_format, log_level, **kwargs)

    def add_file_handler(
        self,
        filename: str,
        mode: str = "a",
        encoding: str = "utf-8",
        log_format: str = LOG_FORMAT_BASIC,
        log_level: int = logging.DEBUG,
        **kwargs
    ) -> Self:
        """Add handler that writes to file"""
        return self.add_handler(
            logging.FileHandler,
            log_format,
            log_level,
            filename=filename,
            mode=mode,
            encoding=encoding,
            **kwargs
        )

    def build(self) -> logging.Logger:
        """Returns build logger"""
        return self.logger
