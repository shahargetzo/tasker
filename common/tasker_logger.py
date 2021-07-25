import logging
import os
from logging.handlers import RotatingFileHandler

from common import constants

os.makedirs(constants.logging_dir, exist_ok=True)


class Logger:

    def __init__(self, handler_name: str):
        self.logger = logging.getLogger('tasker')
        formatter = logging.Formatter(
            f'%(asctime)s - %(name)s - {os.getpid()} - {handler_name} - %(levelname)s - %(message)s')
        fh = RotatingFileHandler(os.path.join(constants.logging_dir, 'tasker.log'), maxBytes=200000, backupCount=4)
        fh.setFormatter(formatter)
        fh.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        ch.setLevel(logging.DEBUG)
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def error(self, message: str):
        self.logger.error(message)

    def info(self, message: str):
        self.logger.info(message)

    def debug(self, message: str):
        self.logger.debug(message)

    def warning(self, message: str):
        self.logger.warning(message)
