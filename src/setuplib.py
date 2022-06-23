import os
import sys
import json
import logging
from src.fslib import FsLib

class SetupLib:

    def __init__(self, id=0, name=""):
        self.id = id
        self.name = name
        self.logger = logging.getLogger(__name__)

    def validate(self, setup):
        self.method = "setuplib.validate()"
        message = ""
        side1 = False
        side2 = False
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
            if str(ds["Source"]).strip() == "":
                message = f"Source is missing"
            if str(ds["Separator"]).strip() == "":
                message = f"Separator is missing"
            if len(ds["Field"]) == 0:
                message = f"Field definition not found"
            if len(ds["Type"]) == 0:
                message = f"Type definition not found"
            if len(ds["Mask"]) == 0:
                message = f"Mask definition not found"
            if len(ds["Field"]) != len(ds["Type"]):
                message = f"Field and Type definition are different"
            if len(ds["Field"]) > 0 and len(ds["Field"]) != len(ds["Mask"]):
                message = f"Field and Mask definition are different"
        if side1 == False:
            message = f"Configuration for side 1 not found"
        if side2 == False:
            message = f"Configuration for side 2 not found"
        if message != "":
            self.logger.info(f"{self.method}: {message}")
            os.system("cls")
            print(message)
            return False
        self.logger.info(f"{self.method}: {self.name.strip()} sucessfuly validated")
        return True

    def get_recon_info(self):
        fslib = FsLib()
        self.method = "setuplib.get_recon_info()"
        path = fslib.get_dir_etc("Saldo x Extrato.json")
        setup = fslib.get_json(path)
        self.logger.info(f"{self.method}: Setup loaded sucessfuly")
        return setup