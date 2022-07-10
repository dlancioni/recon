import os
import sys
import json
import logging
from src.fslib import FsLib
from src.utillib import UtilLib
from src.msglib import MsgLib
from src.cfglib import ConfigLib
from src.baselib import BaseLib

msglib = MsgLib()
cfglib = ConfigLib()

class SetupLib(BaseLib):

    def __init__(self, id=0, name=""):
        self.id = id
        self.name = name
        self.error = ""
        self.logger = logging.getLogger(__name__)
    
    def validate_tag(self, session, recon, field, mandatory=False):
        """ dynamic validator """                
        field = msglib.get_value(msglib.field, field)
        if not field in recon:
            raise Exception(msglib.get_value(msglib.validation, "M1", [session, field]))
        if mandatory:
            if str(recon[field]).strip() == "":
                raise Exception(msglib.get_value(msglib.validation, "M2", [field]))

    def validate_info(self, recon):
        """ validate key info """
        session = ""
        self.validate_tag(session, recon, "ID", True)
        self.validate_tag(session, recon, "NAME", True)
        self.validate_tag(session, recon, "DESC", True)
        field = msglib.get_value(msglib.field, "ID")
        id = str(recon[field]).strip()
        if int(id) <= 0: raise Exception(msglib.get_value(msglib.validation, "M3", [field]))
        
    def validate_datasource(self, recon):
        """ validate datasources """        
        sds = msglib.get_value(msglib.field, "DTSC")
        sfd = msglib.get_value(msglib.field, "FLDS")
        session = sds
        self.validate_tag(session, recon, "DTSC")
        ds = msglib.get_value(msglib.field, "DTSC")
        datasources = recon[ds]
        for i in range(0, len(datasources)):
            session = sds
            tag = recon[ds][i]
            self.validate_tag(session, tag, "SIDE", True)
            self.validate_tag(session, tag, "NAME", True)
            self.validate_tag(session, tag, "PATH", False)
            self.validate_tag(session, tag, "FILE", True)
            self.validate_tag(session, tag, "SEPT", True)
            """ validate fields """
            self.validate_tag(session, recon[ds][i], "FLDS")
            field = msglib.get_value(msglib.field, "FLDS")
            fields = recon[ds][i][field]
            for j in range(0, len(fields)):
                session = f"{sds}/{sfd}"
                tag = recon[ds][i][field][j]
                self.validate_tag(session, tag, "NAME", True)
                self.validate_tag(session, tag, "TYPE", True)
                self.validate_tag(session, tag, "VLUE", False)
                self.validate_tag(session, tag, "MASK", False)
                
    def validate_recon(self, recon):
        """ validate conciliations """
        src = msglib.get_value(msglib.field, "RECN")
        sfd = msglib.get_value(msglib.field, "FLDS")        
        session = ""
        self.validate_tag(session, recon, "RECN")
        rc = msglib.get_value(msglib.field, "RECN")
        recons = recon[rc]
        for i in range(0, len(recons)):
            session = msglib.get_value(msglib.field, "RECN")
            tag = recon[rc][i]
            self.validate_tag(session, tag, "RULE", True)
            """ validate fields """
            self.validate_tag(session, recons[i], "FLDS")
            field = msglib.get_value(msglib.field, "FLDS")
            fields = recon[rc][i][field]
            for j in range(0, len(fields)):
                session = f"{src}/{sfd}"
                tag = recon[rc][i][field][j]
                self.validate_tag(session, tag, "TYPE", True)
                self.validate_tag(session, tag, "NAME", True)

    def validate(self, recon):
        """ full validation, structure and data """
        self.method = "setuplib.validate()"
        try:
            self.validate_info(recon)
            self.validate_datasource(recon)
            self.validate_recon(recon)
        except BaseException as err:
            msg = f"Validation error -> {str(err)}"
            self.log_error(msg)
            raise Exception(msg)