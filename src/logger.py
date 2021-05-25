import logging

from logging.handlers import RotatingFileHandler

FILE            = '/tmp/yolinkhome.log'
FILE_MAXSIZE    = 10 * 1024 * 1024 # 10MB
FILE_BACKUP_CNT = 2

def getLogger(name, fname=FILE, maxBytes=FILE_MAXSIZE, backupCount=FILE_BACKUP_CNT):
    """
    Configure Logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)                                                                                  

    # String format log
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s:%(module)s:%(levelname)s - %(message)s',
            "%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    rotate_file_handler = RotatingFileHandler(fname, maxBytes, backupCount)

    logger.addHandler(rotate_file_handler)
    return logger
