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

    def get_datatype(self, datatype):
        datatype = dt.strip().lower()
        if datatype in ["integer", "inteiro"]:        
            return "Integer"
        if datatype in ["decimal"]:
            return "Decimal"
        if datatype in ["text", "texto"]:
            return "Text"
        if datatype in ["datetime", "datahora"]:
            return "datetime"
        return datatype

    def get_function(self, func=""):
        func = func.strip().lower()
        if func in ["sum", "somatoria"]:
            return "sum"
        if func in ["max", "maximo"]:
            return "max"
        if func in ["min", "minimo"]:
            return "min"
        if func in ["avg", "media"]:
            return "avg"
        if func in ["round", "arredondar"]:
            return "round"
        return func

    def validate_json(self):
        pass

    def validate_key(self, setup):
        id = str(setup["Id"]).strip()
        name = str(setup["Name"]).strip()
        ds = str(setup["Description"]).strip()
        if id == "":
            field = msglib.get_value(msglib.field, "F1")
            msg = msglib.get_value(msglib.validation, "M1", [field])
            raise Exception(msg)
        if int(id) <= 0:
            field = msglib.get_value(msglib.field, "F1")
            msg = msglib.get_value(msglib.validation, "M2", [field])
            raise Exception(msg)
        if name == "":
            field = msglib.get_value(msglib.field, "F2")
            msg = msglib.get_value(msglib.validation, "M1", [field])
            raise Exception(msg)
        if ds == "":
            field = msglib.get_value(msglib.field, "F3")
            msg = msglib.get_value(msglib.validation, "M1", [field])
            raise Exception(msg)

    def validate_sides(self, setup):
        msg = ""
        side1, side2 = False, False
        for ds in setup["Datasources"]:
            if str(ds["Side"]) != "1" and str(ds["Side"]) != "2":
                return f"Side is invalid or missing, must be 1 or 2"
            if str(ds["Side"]) == "1":
                side1 = True
            if str(ds["Side"]) == "2":
                side2 = True
        if side1 == False:
            return f"Configuration for side 1 not found"
        if side2 == False: 
            return f"Configuration for side 2 not found"
        return ""        

    def validate_datasources(self, setup):
        for ds in setup["Datasources"]:
            side = ds["Side"]
            if str(ds["Name"]).strip() == "": 
                return f"Side {side}: name is missing"
            if str(ds["File"]).strip() == "":
                return f"Side {side}: file is missing"
            if str(ds["Separator"]).strip() == "":
                return f"Side {side}: separator is missing"
        return ""

    def validate_fields(self, setup):        
        for datasource in setup["Datasources"]:
            name = datasource["Name"]
            fields = datasource["Fields"]
            if len(fields) == 0:
                return f"Datasource {name}: Field definition not found"
            for field in fields:
                if str(field["Id"]).strip() == "":
                    return f"Datasource {name}: Field Id is mandatory"
                if str(field["Name"]).strip() == "":
                    return f"Datasource {name}: Field Name is mandatory"
                if str(field["Type"]).strip() == "":
                    return f"Datasource {name}: Field Type is mandatory"
        return ""

    def validate(self, setup):
        self.method = "setuplib.validate()"
        msg = ""
        if msg == "":            
            msg = self.validate_sides(setup)
        if msg == "":            
            msg = self.validate_datasources(setup)
        if msg == "":            
            msg = self.validate_fields(setup)
            
        if msg != "":
            msg = f"{self.name.strip()} is invalid -> {msg}"
        else:
            msg = f"{self.name.strip()} sucessfuly validated"
        return True if self.error == "" else False