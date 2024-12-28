import logging
from logging.handlers import RotatingFileHandler
import json
from .models import DefaultLogger

class LoggerSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LoggerSingleton, cls).__new__(cls)
            cls._instance._configure_logger()
        return cls._instance

    def _configure_logger(self):
        self.logger = logging.getLogger("custom_logger")
        self.logger.setLevel(logging.INFO)

        file_handler = RotatingFileHandler("app.log", maxBytes=5*1024*1024, backupCount=5)
        file_format = logging.Formatter('%(message)s')
        file_handler.setFormatter(file_format)

        console_handler = logging.StreamHandler()
        console_format = logging.Formatter('%(message)s')
        console_handler.setFormatter(console_format)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger

    def log_transaction(self, log_entry: DefaultLogger):
        log_method = getattr(self.logger, log_entry.level.lower(), self.logger.info)
        log_method(log_entry.json())