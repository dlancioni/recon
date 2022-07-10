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
    
    def validate_tag(self, recon, field, mandatory=False):
        field = msglib.get_value(msglib.field, field)
        if not field in recon:
            raise Exception(msglib.get_value(msglib.validation, "M1", [field]))
        if mandatory:
            if str(recon[field]).strip() == "":
                raise Exception(msglib.get_value(msglib.validation, "M2", [field]))

    def validate_info(self, recon):
        # validate info
        self.validate_tag(recon, "ID", True)
        self.validate_tag(recon, "NAME", True)
        self.validate_tag(recon, "DESC", True)
        # validate id
        field = msglib.get_value(msglib.field, "ID")
        id = str(recon[field]).strip()
        if int(id) <= 0: raise Exception(msglib.get_value(msglib.validation, "M3", [field]))
        
    def validate_datasource(self, recon):        
        # validate datasources
        self.validate_tag(recon, "DTSC")
        ds = msglib.get_value(msglib.field, "DTSC")
        datasources = recon[ds]
        for i in range(0, len(datasources)):
            tag = recon[ds][i]
            self.validate_tag(tag, "SIDE", True)
            self.validate_tag(tag, "NAME", True)
            self.validate_tag(tag, "PATH", False)
            self.validate_tag(tag, "FILE", True)
            self.validate_tag(tag, "SEPT", True)
            # validate fields
            self.validate_tag(recon[ds][i], "FLDS")
            field = msglib.get_value(msglib.field, "FLDS")
            fields = recon[ds][i][field]
            for j in range(0, len(fields)):
                tag = recon[ds][i][field][j]
                self.validate_tag(tag, "NAME", True)
                self.validate_tag(tag, "TYPE", True)
                self.validate_tag(tag, "VLUE", False)
                self.validate_tag(tag, "MASK", False)

    def validate(self, recon):
        self.method = "setuplib.validate()"
        try:
            self.validate_info(recon)
            self.validate_datasource(recon)
        except BaseException as err:
            msg = f"Validation error -> {str(err)}"
            self.log_error(msg)
            raise Exception(msg)