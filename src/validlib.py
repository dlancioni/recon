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
        if field_type.strip().lower() not in const.DATATYPE:
            raise Exception(msglib.get("V11", [field_type]))

    def validate_tag(self, config, field_name, field_type="text", mandatory=True, domain=[]):
        tag_name = setuplib.tag_name(config, field_name)
        tag_value = config[tag_name]                
        self.validate_field_type(field_type)        
        if field_type.lower() in const.DATATYPE_NUMERIC:
            self.validate_numeric(tag_name, tag_value)
        if mandatory:
            if str(tag_value) == "":
                raise Exception(msglib.get("V2", [tag_name]))
        if domain != []:
            if tag_value.lower() not in domain:
                raise Exception(msglib.get("V21", [tag_name, str(domain)]))

    """ Validate json header """
    def validate_info(self, config):
        loglib = LogLib("ValidationLib", "validate_info")
        self.validate_tag(config, "Id", "Integer")
        self.validate_tag(config, "Name")
        self.validate_tag(config, "Description")

    """ Validate datasources """
    def validate_datasource_info(self, datasource):
        loglib = LogLib("ValidationLib", "validate_datasource_info")
        self.validate_tag(datasource, "Name")
        self.validate_tag(datasource, "Type")
        self.validate_tag(datasource, "Side", "Integer", True, const.SIDES)

    def validate_datasource_file(self, datasource):
        loglib = LogLib("ValidationLib", "validate_datasource_file")
        self.validate_datasource_info(datasource)
        self.validate_tag(datasource, "Path")
        self.validate_tag(datasource, "File")
        self.validate_tag(datasource, "Start")

    def validate_datasource_field(self, datasource, type):
        loglib = LogLib("ValidationLib", "validate_datasource_field")
        for field in datasource[setuplib.tag_name(datasource, "Fields")]:
            self.validate_tag(field, "Position")
            if type == const.DATASOURCES[4]:
                self.validate_tag(field, "Size")
            self.validate_tag(field, "Name")
            self.validate_tag(field, "Type", "Text", True, const.DATATYPE)

    def validate_datasource_file_delimiter(self, datasource):
        loglib = LogLib("ValidationLib", "validate_datasource_file_delimiter")
        self.validate_datasource_file(datasource)
        self.validate_tag(datasource, "Delimiter")
        self.validate_datasource_field(datasource, const.DATASOURCES[2])

    def validate_datasource_file_positional(self, datasource):
        loglib = LogLib("ValidationLib", "validate_datasource_file_positional")
        self.validate_datasource_file(datasource)
        self.validate_datasource_field(datasource, const.DATASOURCES[4])

    def validate_datasource_file_excel(self, datasource):
        loglib = LogLib("ValidationLib", "validate_datasource_file_excel")
        self.validate_datasource_file(datasource)
        self.validate_tag(datasource, "Sheet")
        self.validate_datasource_field(datasource, const.DATASOURCES[3])

    def validate_datasource_db(self, datasource):
        loglib = LogLib("ValidationLib", "validate_datasource_db")
        self.validate_datasource_info(datasource)
        self.validate_tag(datasource, "Connector")
        self.validate_tag(datasource, "Query")
        self.validate_datasource_field(datasource, const.DATASOURCES[1])

