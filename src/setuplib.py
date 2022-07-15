import os
import sys
import json
import logging
from src.fslib import FsLib
from src.msglib import MsgLib
from src.baselib import BaseLib
from src.utillib import UtilLib
from src.cfglib import ConfigLib
from src.loglib import LogLib

msglib = MsgLib()
cfglib = ConfigLib()

class SetupLib(BaseLib):

    def __init__(self, id=0, name=""):
        self.id = id
        self.name = name
        self.error = ""
        self.logger = logging.getLogger(__name__)
    
    def validate_tag(self, session, recon, fields, mandatory=False):
        if mandatory:
            field = self.tagf(recon, fields[0], fields[1])
            value = self.tagv(recon, fields[0], fields[1])
            if str(value) == "":
                raise Exception(msglib.get_value(msglib.validation, "M2", [field]))

    def validate_info(self, recon):
        loglib = LogLib("Setuplib", "validate_info")
        session = ""
        self.validate_tag(session, recon, ["Id", "Id"], True)
        self.validate_tag(session, recon, ["Name", "Nome"], True)
        self.validate_tag(session, recon, ["Description", "Descricao"], True)
        field = self.tagf(recon, "Id", "Id")
        value = self.tagv(recon, "Id", "Id")
        if int(value) <= 0: raise Exception(msglib.get_value(msglib.validation, "M3", [field]))
        
    def validate_datasource(self, recon):
        loglib = LogLib("Setuplib", "validate_datasource")
        session = ""
        tag_ds = self.tagf(recon, "Datasources", "Dados")
        datasources = recon[tag_ds]
        for i in range(0, len(datasources)):
            session = tag_ds
            values = recon[tag_ds][i]
            self.validate_tag(session, values, ["Side", "Lado"], True)
            self.validate_tag(session, values, ["Name", "Nome"], True)
            self.validate_tag(session, values, ["Path", "Caminho"], False)
            self.validate_tag(session, values, ["File", "Arquivo"], True)
            self.validate_tag(session, values, ["Separator", "Separador"], True)
            """ validate fields """
            self.validate_tag(session, recon[tag_ds][i], ["Fields", "Campos"])
            tag_field = self.tagf(recon[tag_ds][i], "Fields", "Campos")
            fields = recon[tag_ds][i][tag_field]
            for j in range(0, len(fields)):
                session = f"{tag_ds}/{tag_field}"
                values = recon[tag_ds][i][tag_field][j]
                self.validate_tag(session, values, ["Name", "Nome"], True)
                self.validate_tag(session, values, ["Type", "Tipo"], True)
                self.validate_tag(session, values, ["Value", "Valor"], False)
                self.validate_tag(session, values, ["Mask", "Mascara"], False)
                
    def validate_recon(self, recon):
        loglib = LogLib("Setuplib", "validate_recon")
        session = ""
        tag_recon = self.tagf(recon, "Recon", "Conciliação")
        recons = recon[tag_recon]
        for i in range(0, len(recons)):
            session = tag_recon
            tag_rule = self.tagf(recon[tag_recon][i], "Rule", "Regra")
            self.validate_tag(session, recon[tag_recon][i], ["Rule", "Regra"], True)
            """ validate fields """
            self.validate_tag(session, recons[i], ["Fields", "Campos"], True)
            tag_fields = self.tagf(recon[tag_recon][i], "Fields", "Campos")
            fields = recon[tag_recon][i][tag_fields]
            for j in range(0, len(fields)):
                session = f"{tag_recon}/{tag_fields}"
                values = recon[tag_recon][i][tag_fields][j]
                self.validate_tag(session, values, ["Type", "Tipo"], True)
                self.validate_tag(session ,values, ["Name", "Nome"], True)

    def validate(self, recon):
        loglib = LogLib("Setuplib", "validate")
        try:
            self.validate_info(recon)
            self.validate_datasource(recon)
            self.validate_recon(recon)
        except BaseException as err:
            msg = f"Validation error -> {str(err)}"
            loglib.log(loglib.ERROR, msg)
            raise Exception(msg)