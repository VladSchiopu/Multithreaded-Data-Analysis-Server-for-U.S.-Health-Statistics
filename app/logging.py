"""Create the logger for showing entering and exiting routes"""
import logging
from logging.handlers import RotatingFileHandler
import time

def create_logger():
    """Create the logger for showing entering and exiting routes"""
    # Create logger
    info_logger = logging.getLogger('webserver')
    info_logger.setLevel(logging.INFO)

    # Configure the rotating file handler
    handler = RotatingFileHandler(
        'webserver.log',
        maxBytes=10485760,  # 10MB per file
        backupCount=5       # Keep 5 backup files
    )

    # Convert formatter to GMT
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    formatter.converter = time.gmtime

    handler.setFormatter(formatter)
    info_logger.addHandler(handler)


    info_logger.info("Logging initialized for webserver")
    return info_logger

logger = create_logger()
