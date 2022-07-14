import os
import sys
import json
import logging
from src.msglib import MsgLib
from src.baselib import BaseLib

msglib = MsgLib()

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
    
