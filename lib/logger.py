"""@Author         :: BABA SHANKAR

@revision History

@DATE [ DD/MM/YYYY]               @Name                   @Remarks

10-06-2023                       winteck                 This module is to generate log files
"""

import logging
import os
import sys
import time
from logging.handlers import TimedRotatingFileHandler

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/logs" #H:\pystorage_verificaion/logs
# print(os.path.abspath(__file__))#H:\pystorage_verificaion\lib\logger.py
# print(os.path.dirname(os.path.abspath(__file__)))#H:\pystorage_verificaion\lib
# print(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #H:\pystorage_verificaion
# print(path)#H:\pystorage_verificaion/logs


FORMATTER = logging.Formatter("%(asctime)s %(levelname)s %(filename)s'' %(funcName)s %(lineno)s :: %(message)s")
# %(asctime)s: Represents the timestamp of the log record in the format specified by asctime`.
# %(levelname)s: Represents the log level of the log record, such as DEBUG, INFO, WARNING, ERROR, or CRITICAL.
# %(filename)s: Represents the name of the source file where the logging call was made.
# '': This appears to be an empty string literal and does not serve any purpose in this format string.
# %(funcName)s: Represents the name of the function or method where the logging call was made.
# %(lineno)s: Represents the line number in the source file where the logging call was made.
# ::: This appears to be a separator between the location information and the log message.
# %(message)s: Represents the actual log message provided by the user.
dd = time.strftime("%Y-%m-%d")
LOG_FILE = "{}/".format(path) + dd #H:\pystorage_verificaion/logs/2024-02-26
def mkdir_p(path):
    if not os.path.exists(path):# cheack for the file if wnot exit it will create
        os.makedirs(path)
def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)#This line creates an instance of the StreamHandler class, which handles log messages by sending them to a specified stream (in this case, sys.stdout).
    console_handler.setFormatter(FORMATTER)# create the formatter for the console only not  in log file
    return console_handler
def get_file_handler(arg1):
    temp1 = LOG_FILE + "_" + arg1# location of file H:\pystorage_verificaion/logs/2024-02-26
    mkdir_p(temp1)# to create a dir
    temp = os.path.basename(temp1) #2024-02-26_fio_test
    # import re
    # temp = re.sub(r"^\d{4}\d{2}\d{2}_", r"", temp)
    # out = os.environ.get('PYTEST_CURRENT_TEST', "a:b").split(':')[-1].split(' ')[0]
    # if out == None:
    #     out = "hi i am baba"
    # print("DEBUG pytest", out)
    file_handler = TimedRotatingFileHandler(temp1 + "/" + temp + ".log", when="H", interval=48)#['/dev/sda', '/dev/sdb', '/dev/sdc', '/dev/sdd', '/dev/sde', '/dev/sdf', '/dev/sdg', '/dev/sdh']
    #<TimedRotatingFileHandler H:\pystorage_verificaion\logs\2024-02-26_fio_test\2024-02-26_fio_test.log (NOTSET)>
    file_handler.setFormatter(FORMATTER)# formatter for the log file only not console 2024-02-26 15:14:51,099 INFO Storage_lib.py'' <module> 28 :: ['/dev/sda', '/dev/sdb', '/dev/sdc', '/dev/sdd', '/dev/sde', '/dev/sdf', '/dev/sdg', '/dev/sdh']
    return file_handler

#    2024-02-26 15:14:51,099 INFO Storage_lib.py'' <module> 28 :: ['/dev/sda', '/dev/sdb', '/dev/sdc', '/dev/sdd', '/dev/sde', '/dev/sdf', '/dev/sdg', '/dev/sdh']
#
def get_logger(logger_name, arg1=""):
    logger = logging.getLogger(logger_name)# retrieves or creates a logger object with the given name
    logger.setLevel(logging.DEBUG) #better to have too much log than not enough
    logger.addHandler(get_console_handler())#It adds two handlers to the logger: one for logging to the console and another for logging to a file.
    logger.addHandler(get_file_handler(arg1)) #creating folder and file
    return logger

def get_logname():
      return LOG_FILE

def get_logpath():
    return path
