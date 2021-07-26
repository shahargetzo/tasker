import logging
import os
from logging.handlers import RotatingFileHandler

from src.common import constants

os.makedirs(constants.logging_dir, exist_ok=True)


class Logger:

    def __init__(self, handler_name: str):
        self.logger = logging.getLogger('tasker')
        formatter = logging.Formatter(
            f'%(asctime)s - %(name)s - {os.getpid()} - {handler_name} - %(levelname)s - %(message)s')
        log_path = os.path.join(constants.logging_dir, f'tasker_{handler_name}.log')
        fh = RotatingFileHandler(log_path, maxBytes=200000, backupCount=4)
        fh.setFormatter(formatter)
        fh.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        ch.setLevel(logging.DEBUG)
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
        print(f'log path: {log_path}')

    def error(self, message: str):
        print(f' - error - {message}')
        self.logger.error(message)

    def info(self, message: str):
        print(f' - info - {message}')
        self.logger.info(message)

    def debug(self, message: str):
        print(f' - debug - {message}')
        self.logger.debug(message)

    def warning(self, message: str):
        print(f' - warning - {message}')
        self.logger.warning(message)
