#!/usr/bin/env python

from netmiko import ConnectHandler, NetmikoTimeoutException
import sys
import base64
import logging
from logging.handlers import TimedRotatingFileHandler

# Complexe logger with format and time rotation
FORMATTER = logging.Formatter('%(asctime)s — %(name)s — %(levelname)s — %(message)s')
LOG_FILE = '../logs/netmiko.log'


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler():
    file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight', backupCount=7)
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name, log_level=logging.DEBUG):
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    logger.propagate = False
    return logger


# logger = get_logger('netmiko')  # uncomment to activate/deactive complexe logger
# end of region

# Simple logger
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)
logger = logging.getLogger('netmiko')
# end of region


base_dir = '../_file_input/'
ip_address = '127.0.0.1'
port = 55000  # default is 22 but for docker test purpose it can't be 22 on localhost
command_file = 'test_config.conf'
device_os = 'cisco_nxos'
username = 'root'  # gaasanspy
password = 'root'  # base64.b64decode('ZC5BdmlkMyFiRWF1')

try:
    with ConnectHandler(device_type=device_os, ip=ip_address, username=username,
                        password=password) as net_connect:
        conf_file = f'{base_dir}{command_file}'
        net_connect.enable()  # might not be needed on prod enable mode seem to be active all the time
        output = net_connect.send_config_from_file(conf_file)
        output += net_connect.save_config()

        print()
        print(output)
        print()
except NetmikoTimeoutException as timeout:
    print(timeout)