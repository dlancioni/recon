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
        self.logger = logging.getLogger(__name__)
        
    def validate_fields(self, fields):
        message = ""
        if len(fields) == 0:
            message = f"Field definition not found"
        for field in fields:
            if len(field["name"]) == 0:
                message = f"Name is mandatory"
            if len(field["type"]) == 0:
                message = f"Type is mandatory"
        return message

    def validate(self, setup):
        self.method = "setuplib.validate()"
        message = ""
        side1 = False
        side2 = False
        utillib = UtilLib()
        self.logger.info(f"{self.method}: Validating {self.name}")
        if str(setup["Id"]).strip() == "":
            message = f"Id is missing"
        if str(setup["Name"]).strip() == "": 
            message = f"Name is missing"
        for ds in setup["Datasources"]:
            if str(ds["Side"]) != "1" and str(ds["Side"]) != "2":
                message = f"Side is invalid or missing, must be 1 or 2"
            if str(ds["Side"]) == "1":
                side1 = True
            if str(ds["Side"]) == "2":
                side2 = True
            if str(ds["Name"]).strip() == "":
                message = f"Side name is missing"
            if str(ds["File"]).strip() == "":
                message = f"File is missing"
            if str(ds["Separator"]).strip() == "":
                message = f"Separator is missing"                
            message = self.validate_fields(ds["Fields"])
        if side1 == False:
            message = f"Configuration for side 1 not found"
        if side2 == False:
            message = f"Configuration for side 2 not found"
        if message != "":
            message = f"{self.method}: Invalid Recon -> {str(message)}"
            utillib.log(message)
            self.logger.error(message)                        
            return False
        self.logger.info(f"{self.method}: {self.name.strip()}sucessfuly validated")
        return True

    def get_recon_info(self, recon):
        fslib = FsLib()
        self.method = "setuplib.get_recon_info()"
        path = fslib.get_dir_etc(recon)
        setup = fslib.get_json(path)
        self.logger.info(f"{self.method}: Setup loaded sucessfuly")
        return setup