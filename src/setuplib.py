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
        
    def get_recon_info(self, recon):
        fslib = FsLib()
        self.method = "setuplib.get_recon_info()"
        path = fslib.get_dir_etc(recon)
        setup = fslib.get_json(path)
        self.logger.info(f"{self.method}: Setup loaded sucessfuly")
        return setup        

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
        self.logger.info(f"{self.method}: Validating {self.name}")       
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
        utillib = UtilLib()
        utillib.log(msg)
        self.logger.error(f"{self.method}: {msg}")        
        return True if self.error == "" else False