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
fslib = FsLib()

class SetupLib(BaseLib):

    def __init__(self, id=0, name=""):
        self.id = id
        self.name = name
        self.error = ""
        self.logger = logging.getLogger(__name__)
        
    def tag_def(self):
        tags = {
            "Id":"Id",
            "Name":"Nome",
            "Description":"Descrição",
            "Datasources":"Dados",
            "Fields":"Campos",
            "Side":"Lado",
            "Path":"Caminho",
            "File":"Arquivo",
            "Separator":"Separador",
            "Start":"Inicio",
            "Type":"Tipo",
            "Value":"Valor",
            "Mask":"Mascara",
            "Recon":"Conciliação",
            "Rule":"Regra",
            "Tolerance":"Tolerancia",
            "Type":"Tipo",
            "Function":"Funcao"
        }
        return tags
        
    def translate(self, tag_en=""):
        tag_pt = ""
        tag_en = tag_en.capitalize()
        tags = self.tag_def()
        tag_pt = tags[tag_en]
        if tag_pt.strip() == "":
            raise Exception("tag_pt not found in setuplib.translate()")
        return tag_pt
    
    def validate_tag(self, recon, field, mandatory=True):
        if mandatory:
            tag_name = self.tag_name(recon, field)
            tag_value = recon[tag_name]
            if str(tag_value) == "":
                raise Exception(msglib.get("V2", [field]))

    def validate_info(self, recon):
        loglib = LogLib("Setuplib", "validate_info")
        session = ""
        self.validate_tag(recon, "Id")
        self.validate_tag(recon, "Name")
        self.validate_tag(recon, "Description")
        field = self.tag_name(recon, "Id")
        value = self.tag_value(recon, "Id")
        if int(value) <= 0:
            raise Exception(msglib.get("V3", [field]))

    def validate_side(self, recon):
        loglib = LogLib("Setuplib", "validate_side")
        datasources = self.tag_value(recon, "Datasources")
        for datasource in datasources:
            name = self.tag_value(datasource, "Name")
            fields = self.tag_value(datasource, "Fields")
            if len(fields) == 0:
                raise Exception(msglib.get("V6", [name]))
        
    def validate_datasource(self, recon):
        loglib = LogLib("Setuplib", "validate_datasource")
        session = ""
        tag_ds = self.tag_name(recon, "Datasources")
        datasources = recon[tag_ds]
        for i in range(0, len(datasources)):
            session = tag_ds
            values = recon[tag_ds][i]
            self.validate_tag(values, "Side")
            self.validate_tag(values, "Name")
            self.validate_tag(values, "Path", False)
            self.validate_tag(values, "File")
            self.validate_tag(values, "Separator")
            self.validate_tag(values, "Start")
            """ validate fields """
            self.validate_tag(recon[tag_ds][i], "Fields")
            tag_field = self.tag_name(recon[tag_ds][i], "Fields")
            fields = recon[tag_ds][i][tag_field]
            for j in range(0, len(fields)):
                session = f"{tag_ds}/{tag_field}"
                values = recon[tag_ds][i][tag_field][j]
                self.validate_tag(values, "Id")
                self.validate_tag(values, "Name")
                self.validate_tag(values, "Type")
                self.validate_tag(values, "Value", False)
                self.validate_tag(values, "Mask", False)

    def validate_recon_rules(self, recon):
        loglib = LogLib("Setuplib", "validate_recon_rules")
        rules = self.tag_value(recon, "Recon")
        for rule in rules:
            name = self.tag_value(rule, "Rule")
            fields = self.tag_value(rule, "Fields")
            if len(fields) == 0:
                raise Exception(msglib.get("V7", [name]))

    def validate_recon(self, recon):
        loglib = LogLib("Setuplib", "validate_recon")
        session = ""
        tag_recon = self.tag_name(recon, "Recon")
        recons = recon[tag_recon]
        for i in range(0, len(recons)):
            session = tag_recon
            tag_rule = self.tag_name(recon[tag_recon][i], "Rule")
            self.validate_tag(recon[tag_recon][i], "Rule")
            """ validate fields """
            self.validate_tag(recons[i], "Fields")
            tag_fields = self.tag_name(recon[tag_recon][i], "Fields")
            fields = recon[tag_recon][i][tag_fields]
            for j in range(0, len(fields)):
                session = f"{tag_recon}/{tag_fields}"
                values = recon[tag_recon][i][tag_fields][j]
                self.validate_tag(values, "Type")
                self.validate_tag(values, "Name")

    def validate(self, recon):
        loglib = LogLib("Setuplib", "validate")
        try:
            self.validate_info(recon)
            self.validate_side(recon)
            self.validate_datasource(recon)
            self.validate_recon_rules(recon)
            self.validate_recon(recon)
        except BaseException as err:
            cat = msglib.get("E4")
            msg = f"{cat} -> {str(err)}"            
            loglib.log(loglib.ERROR, msg)
            raise Exception(msg)
        
    def open_recon(self, recon):
        msg = ""
        if type(recon) == dict:
            return recon
        else:
            try:              
                filename = str(recon.split(".")[0]) +".cfg"
                path = cfglib.get(2)
                path = fslib.get_path_recon(path, filename)
                msg = msglib.get("V4", [path])
                recon = fslib.open_json(path)
            except json.decoder.JSONDecodeError:
                print("There was a problem accessing the equipment data.")
            except BaseException as err:
                raise Exception(msg)
        return recon

    def tagfv(self, doc, tag_en):
        f, v = "", ""
        tag_pt = self.translate(tag_en)
        tag_en = tag_en.capitalize().strip()
        tag_pt = tag_pt.capitalize().strip()
        if tag_en in doc:
            f = tag_en
            v = doc[tag_en]
            return f, v
        if tag_pt in doc:
            f = tag_pt
            v = doc[tag_pt]
        return f, v

    def tag_name(self, doc, tag_en="", mandatory=True):
        f, v = self.tagfv(doc, tag_en)
        if mandatory == True:
            if f == "":
                msglib = MsgLib()
                msg = f"{tag_en}/{tag_pt}"
                msg = msglib.get("V5", [msg])
                raise Exception(msg)
        return f

    def tag_value(self, doc, tag_en="", mandatory=True):
        f, v = self.tagfv(doc, tag_en)
        return v