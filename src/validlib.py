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

fslib = FsLib()
msglib = MsgLib()
cfglib = ConfigLib()
setuplib = SetupLib()
utillib = UtilLib()

class ValidationLib(BaseLib):

    def __init__(self, id=0, name=""):
        self.id = id
        self.name = name
        self.error = ""
        self.logger = logging.getLogger(__name__)

    def validate_numeric(self, field_name="", field_value=""):
        if str(field_value).isnumeric() == False:
            raise Exception(msglib.get("V12", [field_name, field_value]))

    def validate_field_name(self, field_name):
        invalid_char = ""
        valid_char = list("abcdefghijklmnopqrstuvwxyzáéíóúÁÉÍÓÚABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789çÇãÃ ")
        for item in field_name:
            if item not in valid_char:
                invalid_char = item
                break
        if invalid_char != "":
            raise Exception(msglib.get("V10", [invalid_char]))

    def validate_field_type(self, field_type=""):
        if field_type.strip().lower() not in const.DATATYPE:
            raise Exception(msglib.get("V11", [field_type]))
        
    def validate_field_mask(self, field_name, field_type="", field_mask=""):
        field_mask = field_mask.strip().upper()
        if field_type.strip().lower() in const.DATATYPE_DECIMAL:
            if field_mask not in [".", ","]:
                raise Exception(msglib.get("V23", [field_name, field_mask]))
        if field_type.strip().lower() in const.DATATYPE_DATETIME:
            if field_mask == "":
                raise Exception(msglib.get("V24", [field_name]))

    def validate_tag(self, config, field_name, field_type="text", mandatory=True, domain=[]):
        tag_name = setuplib.tag_name(config, field_name, False)
        if tag_name != "":
            tag_value = config[tag_name]
            self.validate_field_name(tag_name)
            self.validate_field_type(field_type)           
            if tag_name in ["Mask", "Mascara"]:
                tag_type = config[setuplib.tag_name(config, "Type")]
                self.validate_field_mask(config[setuplib.tag_name(config, "Name")], tag_type, tag_value)
            if field_type.lower() in const.DATATYPE_NUMERIC:
                self.validate_numeric(tag_name, tag_value)
            if mandatory:
                if str(tag_value) == "":
                    raise Exception(msglib.get("V2", [tag_name]))
            if domain != []:
                if tag_value.lower() not in domain:
                    raise Exception(msglib.get("V21", [tag_name, str(domain)]))
                
    def get_fields_datasources(self, config):
        fields = []
        datasources = config[setuplib.tag_name(config, "Datasources")]
        for datasource in datasources:
            datasource_fields = datasource[setuplib.tag_name(datasource, "Fields")]
            for field in datasource_fields:
                field_name = field[setuplib.tag_name(field, "Name")]
                field_type = field[setuplib.tag_name(field, "Type")]
                item = [field_name, field_type]
                if item not in fields:
                    fields.append(item)
        return fields                

    def validate_info(self, config):
        loglib = LogLib("ValidationLib", "validate_info")
        self.validate_tag(config, "Id", "Integer")
        self.validate_tag(config, "Name")
        self.validate_tag(config, "Description")
        self.validate_tag(config, "Results")
        if setuplib.tag_value(config, "Results") not in const.RESULTS:
            raise Exception(msglib.get("V29", [setuplib.tag_value(config, "Results")]))          
        if int(setuplib.tag_value(config, "Id")) <= 0:
            raise Exception(msglib.get("V3", ["Id"]))

    def validate_datasource_info(self, datasource):
        loglib = LogLib("ValidationLib", "validate_datasource_info")
        self.validate_tag(datasource, "Name")
        self.validate_tag(datasource, "Type")
        self.validate_tag(datasource, "Side", "Integer", True, const.SIDES)
        return setuplib.tag_value(datasource, "Type")

    def validate_datasource_file(self, datasource):
        loglib = LogLib("ValidationLib", "validate_datasource_file")
        self.validate_datasource_info(datasource)
        self.validate_tag(datasource, "Path", "Text", False)
        self.validate_tag(datasource, "File")
        self.validate_tag(datasource, "Start", "Integer")

    def validate_datasource_field(self, datasource, type=[]):
        loglib = LogLib("ValidationLib", "validate_datasource_field")
        names = []
        positions = []
        fields = datasource[setuplib.tag_name(datasource, "Fields")]
        name = setuplib.tag_value(datasource, "Name")
        if len(fields) == 0:
            raise Exception(msglib.get("V6", [name]))
        for field in fields:
            self.validate_tag(field, "Position")            
            if type == const.DATASOURCE_POSITIONAL:
                self.validate_tag(field, "Size")                
            self.validate_tag(field, "Name")
            self.validate_tag(field, "Type", "Text", True, const.DATATYPE)
            
            if str(setuplib.tag_value(field, "Type")).lower() in const.DATATYPE_DATETIME + const.DATATYPE_DECIMAL:
                if setuplib.tag_value(field, "Mask", False) == "":
                    raise Exception(msglib.get("V22", [name, setuplib.tag_value(field, "Name"), setuplib.tag_value(field, "Type")]))
                else:    
                    self.validate_tag(field, "Mask", "Text", True)
                    
                    
            names.append(setuplib.tag_value(field, "Name"))
            positions.append(setuplib.tag_value(field, "Position"))
        diff = utillib.diff(names)
        if len(diff) > 0:
            raise Exception(msglib.get("V13", [diff[0], name]))
        diff = utillib.diff(positions)
        if len(diff) > 0:
            raise Exception(msglib.get("V7", [diff[0], name]))

    def validate_datasource_file_delimited(self, datasource):
        loglib = LogLib("ValidationLib", "validate_datasource_file_delimited")
        self.validate_datasource_file(datasource)
        self.validate_tag(datasource, "Delimiter")
        self.validate_datasource_field(datasource)

    def validate_datasource_file_positional(self, datasource):
        loglib = LogLib("ValidationLib", "validate_datasource_file_positional")
        self.validate_datasource_file(datasource)
        self.validate_datasource_field(datasource, const.DATASOURCE_POSITIONAL)

    def validate_datasource_file_excel(self, datasource):
        loglib = LogLib("ValidationLib", "validate_datasource_file_excel")
        self.validate_datasource_file(datasource)
        self.validate_tag(datasource, "Sheet")
        self.validate_datasource_field(datasource)

    def validate_datasource_db(self, datasource):
        loglib = LogLib("ValidationLib", "validate_datasource_db")
        self.validate_datasource_info(datasource)
        self.validate_tag(datasource, "Connector")
        self.validate_tag(datasource, "Query")
        self.validate_datasource_field(datasource)
        
    def validate_datasources(self, config):
        side = 1
        fields = []
        loglib = LogLib("ValidationLib", "validate_datasources")        
        datasources = config[setuplib.tag_name(config, "Datasources")]
        for datasource in datasources:
            if side > 1:
                if len(datasource[setuplib.tag_name(datasource, "Fields")]) == 0:
                    datasource[setuplib.tag_name(datasource, "Fields")] = fields
                    loglib.log(loglib.INFO, "Side 2 has no field definition, copying from side 1")
            type = self.validate_datasource_info(datasource)
            if type in const.DATASOURCE_DELIMITED:
                self.validate_datasource_file_delimited(datasource)
            if type in const.DATASOURCE_POSITIONAL:
                self.validate_datasource_file_positional(datasource)
            if type in const.DATASOURCE_EXCEL:
                self.validate_datasource_file_excel(datasource)
            if type in const.DATASOURCE_DB:
                self.validate_datasource_db(datasource)
            fields = datasource[setuplib.tag_name(datasource, "Fields")]
            side = side + 1
                
    def validate_datasources_sides(self, config):
        loglib = LogLib("ValidationLib", "validate_datasources_sides")
        sides = []
        name1 = []
        name2 = []
        datasources = config[setuplib.tag_name(config, "Datasources")]
        for datasource in datasources:
            sides.append(int(setuplib.tag_value(datasource, "Side")))
            if int(setuplib.tag_value(datasource, "Side")) == 1: name1.append(setuplib.tag_value(datasource, "Name"))
            if int(setuplib.tag_value(datasource, "Side")) == 2: name2.append(setuplib.tag_value(datasource, "Name"))
        sides = list(set(sides))
        if 1 not in sides: raise Exception(msglib.get("V5", [1]))
        if 2 not in sides: raise Exception(msglib.get("V5", [2]))
        for side in range(1,3):
            name = name1 if side == 1 else name2           
            diff = utillib.diff(name)
            if len(list(diff)) > 0:
                raise Exception(msglib.get("V8", [diff[0], side]))
        diff = list(set(name1).intersection(name2))
        if len(diff) > 0:
            raise Exception(msglib.get("V9", [diff[0]]))
        
    def validate_recon(self, config):
        loglib = LogLib("ValidationLib", "validate_recon")
        fields = self.get_fields_datasources(config)
        recon = config[setuplib.tag_name(config, "Recon")]
        for rule in recon:
            rule_name = setuplib.tag_value(rule, "Rule")
            rule_fields = setuplib.tag_value(rule, "Fields")
            for field in rule_fields:
                field_name = setuplib.tag_value(field, "Name", False)
                field_tolerance = setuplib.tag_value(field, "Tolerance", False)                            
                found = False
                for field in fields:
                    if field[0] == field_name:
                        found = True
                        if field_tolerance != "":
                            if str(field[1]).lower() not in const.DATATYPE_NUMERIC:
                                raise Exception(msglib.get("V28", [field_name, rule_name]))                        
                        break
                if found == False:
                    raise Exception(msglib.get("V27", [field_name, rule_name]))

    def validate(self, config):
        loglib = LogLib("ValidationLib", "validate")
        try:
            self.validate_info(config)
            self.validate_datasources(config)
            self.validate_datasources_sides(config)
            self.validate_recon(config)
        except BaseException as err:
            cat = msglib.get("E4")
            msg = f"{cat} {str(err)}"
            loglib.log(loglib.ERROR, msg)
            raise Exception(msg)
