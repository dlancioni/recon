import os
import sys
import json
import logging
from src.fslib import FsLib
from src.utillib import UtilLib
from src.msglib import MsgLib
from src.cfglib import ConfigLib

msglib = MsgLib()
cfglib = ConfigLib()

class SetupLib:

    def __init__(self, id=0, name=""):
        self.id = id
        self.name = name
        self.error = ""
        self.logger = logging.getLogger(__name__)

    def validate_json(self, recon):
        pass
    
    def validate_tag(self, recon, field):
        field = msglib.get_value(msglib.field, field)
        if not field in recon: raise Exception(msglib.get_value(msglib.validation, "M1", [field]))
    
    def validate_mandatory(self, recon, field):
        field = msglib.get_value(msglib.field, field)
        if not field in recon: raise Exception(msglib.get_value(msglib.validation, "M1", [field]))
        if str(recon[field]).strip() == "": raise Exception(msglib.get_value(msglib.validation, "M2", [field]))

    def validate_info(self, recon):
        # mandatory
        self.validate_mandatory(recon, "ID")
        self.validate_mandatory(recon, "NAME")
        self.validate_mandatory(recon, "DESC")
        # valid ID
        field = msglib.get_value(msglib.field, "ID")
        id = str(recon[field]).strip()
        if int(id) <= 0: raise Exception(msglib.get_value(msglib.validation, "M3", [field]))
        
    def validate_datasource(self, recon):
        # valid datasource
        self.validate_tag(recon, "DTSC")
        # valid fields
        field = msglib.get_value(msglib.field, "DTSC")
        self.validate_tag(recon[field][0], "FLDS")
        self.validate_tag(recon[field][1], "FLDS")
        # recon
        self.validate_tag(recon, "RECN")
        # recon/fields
        field = msglib.get_value(msglib.field, "RECN")
        self.validate_tag(recon[field], "FLDS")

    def validate(self, recon):
        self.method = "setuplib.validate()"
        try:
            self.validate_info(recon)
        except BaseException as err:
            msg = f"Validation error -> {str(err)}"
            self.log_error(msg)
            raise Exception(msg)