import logging
import os
from datetime import datetime
import coloredlogs
from pathlib import Path


class Logger:
    """
    Custom logger class with coloredlogs support and file logging.
    Provides structured logging with timestamps and log levels.
    """

    def __init__(self, name=__name__, log_level=None):
        self.logger = logging.getLogger(name)
        
        if log_level is None:
            log_level = os.getenv('LOG_LEVEL', 'INFO')
        
        self.logger.setLevel(getattr(logging, log_level.upper()))
        
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self):
        """
        Setup console and file handlers for logging.
        """
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = log_dir / f'test_run_{timestamp}.log'
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        
        file_format = logging.Formatter(
            '[%(asctime)s] [%(levelname)-8s] [%(name)s] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_format)
        
        self.logger.addHandler(file_handler)
        
        coloredlogs.install(
            level=self.logger.level,
            logger=self.logger,
            fmt='[%(asctime)s] [%(levelname)-8s] [%(name)s] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            level_styles={
                'debug': {'color': 'cyan'},
                'info': {'color': 'green'},
                'warning': {'color': 'yellow', 'bold': True},
                'error': {'color': 'red', 'bold': True},
                'critical': {'color': 'red', 'bold': True, 'background': 'white'}
            }
        )
    
    def debug(self, message):
        self.logger.debug(message)
    
    def info(self, message):
        self.logger.info(message)
    
    def warning(self, message):
        self.logger.warning(message)
    
    def error(self, message):
        self.logger.error(message)
    
    def critical(self, message):
        self.logger.critical(message)
    
    def exception(self, message):
        self.logger.exception(message)


def get_logger(name=__name__, log_level=None):
    """
    Factory function to get a logger instance.
    
    Args:
        name: Logger name (default: caller module name)
        log_level: Log level (default: from env or INFO)
    
    Returns:
        Logger: Configured logger instance
    """
    return Logger(name, log_level)
