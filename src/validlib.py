import os
import re
import sys
import json
import logging
from src.fslib import FsLib
from src.msglib import MsgLib
from src.baselib import BaseLib
from src.utillib import UtilLib
from src.cfglib import ConfigLib
from src.loglib import LogLib
from src.setuplib import SetupLib
from src.constlib import const

msglib = MsgLib()
cfglib = ConfigLib()
fslib = FsLib()
setuplib = SetupLib()


class ValidationLib(BaseLib):

    def __init__(self, id=0, name=""):
        self.id = id
        self.name = name
        self.error = ""
        self.logger = logging.getLogger(__name__)

    def validate_numeric(self, field_name="", field_value=""):
        if str(field_value).isnumeric() == False:
            raise Exception(msglib.get("V12", [field_name, field_value]))

    def validate_field_name(self, field_name=""):
        invalid_char = ""
        valid_char = list("abcdefghijklmnopqrstuvwxyzáéíóúÁÉÍÓÚABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ")
        for item in field_name:
            if item not in valid_char:
                invalid_char = item
                break
        if invalid_char != "":
            raise Exception(msglib.get("V10", [invalid_char]))
        
    def validate_field_type(self, field_type=""):
        datatypes =  ["decimal", "integer", "inteiro", "text", "texto", "datetime", "datahora"]
        if field_type.strip().lower() not in datatypes:
            raise Exception(msglib.get("V11", [field_type]))

    def valid_tag(self, config, field, data_type="text", mandatory=True):
        self.validate_field_type(data_type)
        if mandatory:
            tag_name = setuplib.tag_name(config, field)
            tag_value = config[tag_name]
            if str(tag_value) == "":
                raise Exception(msglib.get("V2", [tag_name]))
        return True    

    def validate_info(self, config):
        loglib = LogLib("ValidationLib", "validate_info")
        self.valid_tag(config, "Id", "Integer")
        self.valid_tag(config, "Name")
        self.valid_tag(config, "Description")


