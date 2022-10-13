from common import Logging
import logging

__all__ = ['Component']

class Component(Logging):

    def __init__(self, logger_name=None, log_level=logging.DEBUG, **kwargs):
        super().__init__(logger_name, log_level, 'component')
        self.kwargs = kwargs

    def _run(self):
        self.logger.info("Hello KMP")