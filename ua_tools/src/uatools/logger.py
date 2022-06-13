import logging, sys, os

WORK_DIR = os.path.realpath(os.path.dirname(os.path.dirname(__file__)))
LOG_FORMATTER = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
LOG_FILE = f'{WORK_DIR}/uatools/logs/ua_vpn_usage.log'


def get_console_handler():
    # each execution will output logs into the console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(LOG_FORMATTER)
    return console_handler


def get_file_handler():
    # each execution will rewrite log file
    file_handler = logging.FileHandler(LOG_FILE, mode='w')
    file_handler.setFormatter(LOG_FORMATTER)
    return file_handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    logger.propagate = False
    return logger
