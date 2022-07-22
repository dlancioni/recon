import os
import sys
import json
import logging
from src.msglib import MsgLib
from src.baselib import BaseLib
from src.fslib import FsLib
from src.cfglib import ConfigLib

fslib = FsLib()
msglib = MsgLib()
cfglib = ConfigLib()

class LogLib(BaseLib):

    def __init__(self, class_name, method_name):
        self.logger = logging.getLogger(__name__)
        self.class_name = class_name
        self.method_name = method_name
        self.ERROR = 1
        self.INFO = 2
        
    def log_info(self, message):
        self.logger.info(message)

    def log_error(self, message):
        self.logger.error(message)
        
    def log(self, level, message):
        msg = f"{self.class_name}.{self.method_name}"
        msg += ": " + message
        if level == self.ERROR:
            self.log_error(msg)
        if level == self.INFO:
            self.log_info(msg)
    
    def create_log_file(self, name):
        fslib = FsLib()
        file_name = f"[log] [{name}].txt" if name != "" else "log.txt"
        log_path = fslib.get_path_log(cfglib.get(1), file_name)
        log_format = "%(asctime)s %(levelname)s %(message)s"
        logging.basicConfig(filename=log_path, filemode="w", datefmt='%Y-%m-%d %H:%M:%S', format=log_format, level=logging.DEBUG, encoding='utf-8')
        logger = logging.getLogger()
        return logger