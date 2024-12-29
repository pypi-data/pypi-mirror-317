import sys

from loguru import logger


class Loger:
    def __init__(self, level="INFO", file=None):
        self.__logger = logger
        self.remove()
        self.add(file or sys.stdout, level=level)

    def __getattr__(self, item):
        return getattr(self.__logger, item)

    def debug(self, msg):
        self.__logger.debug(msg)

    def info(self, msg):
        self.__logger.info(msg)

    def warning(self, msg):
        self.__logger.warning(msg)

    def error(self, msg):
        self.__logger.error(msg)
