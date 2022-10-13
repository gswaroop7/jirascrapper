import logging
import sys

class Logging:
    def __init__(self, logger_name=None, log_level=logging.DEBUG, module_name='helper', **kwargs):
        self.logger = self.get_logger(logger_name, log_level, module_name)

    @classmethod
    def get_logger(cls, logger_name, log_level, module_name):
        name = logger_name or cls.__name__
        logger = logging.getLogger(name)
        if not any(isinstance(handler, logging.StreamHandler) for handler in logger.handlers):
            logger.setLevel(log_level)
            log_handler = logging.StreamHandler(sys.stdout)
            log_handler.setLevel(log_level)
            fmt = logging.Formatter(f'%(asctime)s %(service_name)s {module_name}: line %(lineno)d: '
                                    '%(levelname)s: %(message)s')
            log_handler.setFormatter(fmt)
            logger.addHandler(log_handler)

        logger = logging.LoggerAdapter(logger, {'service_name': cls.__name__})

        return logger