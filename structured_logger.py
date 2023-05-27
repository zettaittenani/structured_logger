from datetime import datetime
import sys
import logging

from pythonjsonlogger import jsonlogger


class CloudLoggingFormatter(jsonlogger.JsonFormatter):
    """
    Log formatter for Google Cloud Logging.
    """
    def parse(self):
        return ["name", "message"]

    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)

        if not log_record.get("timestamp"):
            log_record["timestamp"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%S.%fZ")
        if log_record.get("level"):
            log_record["severity"] = log_record["level"].upper()
        else:
            log_record["severity"] = record.levelname


class StructuredLogger:
    """
    Structured Logger Class for Google Cloud Logging.

    Usage example:
    Logger.info("info log", extra={"key1": "foo", "key2": "bar"})
    => {"name": "transcriber", "message": "hoge", "key1": "foo", "key2": "bar", "timestamp": "2023-06-01T00:00.000000Z", "severity": "INFO"}
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.logger = logging.getLogger("my_app")
        formatter = CloudLoggingFormatter()
        stream = logging.StreamHandler(stream=sys.stdout)
        stream.setFormatter(formatter)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(stream)

    @classmethod
    def debug(cls, msg, *args, **kwargs) -> None:
        cls().debug(msg, *args, **kwargs)

    def _debug(self, msg, *args, **kwargs) -> None:
        self.logger.debug(msg, *args, **kwargs)

    @classmethod
    def info(cls, msg, *args, **kwargs) -> None:
        cls()._info(msg, *args, **kwargs)

    def _info(self, msg, *args, **kwargs) -> None:
        self.logger.info(msg, *args, **kwargs)

    @classmethod
    def warning(cls, msg, *args, **kwargs) -> None:
        cls()._warning(msg, *args, **kwargs)

    def _warning(self, msg, *args, **kwargs) -> None:
        self.logger.warning(msg, *args, **kwargs)

    @classmethod
    def error(cls, msg, *args, **kwargs) -> None:
        cls()._error(msg, *args, **kwargs)

    def _error(self, msg, *args, **kwargs) -> None:
        self.logger.error(msg, *args, **kwargs)

    @classmethod
    def critical(cls, msg, *args, **kwargs) -> None:
        cls()._critical(msg, *args, **kwargs)

    def _critical(self, msg, *args, **kwargs) -> None:
        self.logger.critical(msg, *args, **kwargs)
