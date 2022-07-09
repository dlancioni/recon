import os
import sys
import json
import logging
from src.fslib import FsLib
from src.utillib import UtilLib

class SetupLib:

    def __init__(self, id=0, name=""):
        self.id = id
        self.name = name
        self.error = ""
        self.logger = logging.getLogger(__name__)
        
    def get_mandatory_tags(self):
        return [
            # general
            "Id",
            "Name",
            "Description",
            # Data
            "Datasources",
            "Side",
            "Name",
            "Path",
            "File",
            "Separator",
            # fields
            "Fields",
            "Name",
            "Type",
            "Value",
            "Mask",
            # recon
            "Recons",
            "Rule",
            "Fields"
        ]
    
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
        return ""

    def get_tag(self, tag=""):
        tag = tag.strip().lower()
        # general
        if tag in ["id"]:
            return "Id"
        if tag in ["side", "lado"]:
            return "Side"
        if tag in ["name", "nome"]:
            return "Nome"
        if tag in ["description", "descricao"]:
            return "Description"
        # datasources        
        if tag in ["datasources", "dados"]:
            return "Datasources"
        if tag in ["path", "caminho"]:
            return "Path"
        if tag in ["file", "arquivo"]:
            return "File"
        if tag in ["separator", "separador"]:
            return "Separator"
        # fields
        if tag in ["fields", "campos"]:
            return "Fields"
        # fields
        if tag in ["type", "tipo"]:
            return "Type"
        if tag in ["value", "valor"]:
            return "Value"
        if tag in ["mask", "mascara"]:
            return "Mask"
        # recon
        if tag in ["recons", "conciliacoes"]:
            return "Recons"
        if tag in ["rule", "regra"]:
            return "Rule"
        if tag in ["function", "funcao"]:
            return "Function"
        return ""

    def validate_json(self):
        pass

    def validate_info(self, setup):
        if str(setup["Id"]).strip() == "":
            self.id = -1
            return f"Id is missing"
        if str(setup["Name"]).strip() == "":
            self.name = "[No Name]"
            return f"Name is missing"
        else:
            self.id = setup["Id"]
            self.name = setup["Name"]
        if str(setup["Description"]).strip() == "": 
            return f"Description is missing"
        self.id = setup["Id"]
        self.name = setup["Name"]
        return ""

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
            msg = self.validate_info(setup)
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