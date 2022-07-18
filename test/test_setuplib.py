import os
import sys
import json
import logging
import copy
import unittest
sys.path.insert(1, os.path.abspath(".") + "\\recon\\")

from src.fslib import FsLib
from src.utillib import UtilLib
from src.msglib import MsgLib
from src.cfglib import ConfigLib
from src.corelib import CoreLib

msglib = MsgLib()
corelib = CoreLib()
fslib = FsLib()

class UtilLibTest(unittest.TestCase):
    
    def open_recon(self):
        path = fslib.get_path_recon("", "recon [en_us].cfg")
        recon_en = fslib.open_json(path)
        path = fslib.get_path_recon("", "recon [pt_br].cfg")
        recon_pt = fslib.open_json(path)            
        return recon_en, recon_pt

    def mandatory_info(self):
        recon_en, recon_pt = self.open_recon()
        fields_en = ["Id", "Name", "Description"]
        fields_pt = ["Id", "Nome", "Descrição"]
        for language in ["en-us", "pt-br"]:
            fields = fields_en if language == "en-us" else fields_pt
            i = 0
            for action in ["tagf", "tagv"]:
                for field in fields:
                    recon = copy.copy(recon_en) if language == "en-us" else copy.copy(recon_pt)                    
                    if action == "tagf":
                        us = f"Invalid or missing mandatory tag: {fields_en[i]}/{fields_pt[i]}"
                        pt = f"Tag inválida ou obrigatória: {fields_en[i]}/{fields_pt[i]}"
                        del recon[field]
                    else:
                        us = f"Mandatory field: {field}"
                        pt = f"Campo obrigatório: {field}"
                        recon[field] = ""
                    status, message, reports = corelib.process(recon)
                    if message in [us, pt]: validated = True
                    self.assertEqual(status, False)
                    self.assertEqual(validated, True)
                    status, message = "", ""
                    i += 1

    def mandatory_datasource(self):
        recon_en, recon_pt = self.open_recon()
        fields_en = ["Side", "Name", "Path", "File", "Separator"]
        fields_pt = ["Lado", "Nome", "Caminho", "Arquivo", "Separador"]
        item = 0
        for language in ["en-us", "pt-br"]:
            fields = fields_en if language == "en-us" else fields_pt
            i = 0
            for action in ["tagf", "tagv"]:
                for field in fields:
                    recon = copy.copy(recon_en) if language == "en-us" else copy.copy(recon_pt)
                    session = "Datasources" if language == "en-us" else "Dados"
                    if action == "tagf":
                        us = f"Invalid or missing mandatory tag: {fields_en[i]}/{fields_pt[i]}"
                        pt = f"Tag inválida ou obrigatória: {fields_en[i]}/{fields_pt[i]}"
                        del recon[session][item][field]
                    else:
                        us = f"Mandatory field: {field}"
                        pt = f"Campo obrigatório: {field}"
                        recon[session][item][field] = ""
                    status, message, reports = corelib.process(recon)
                    if message in [us, pt]: validated = True
                    self.assertEqual(status, False)
                    self.assertEqual(validated, True)
                    status, message = "", ""
                    i += 1

    def mandatory_datasource_fields(self):
        recon_en, recon_pt = self.open_recon()
        fields_en = ["Id", "Name", "Type", "Value", "Mask"]
        fields_pt = ["Id", "Nome", "Tipo", "Valor", "Mascara"]
        item = 0
        for language in ["en-us", "pt-br"]:
            fields = fields_en if language == "en-us" else fields_pt
            i = 0
            for action in ["tagf", "tagv"]:
                for field in fields:
                    recon = copy.copy(recon_en) if language == "en-us" else copy.copy(recon_pt)
                    session = "Datasources" if language == "en-us" else "Dados"
                    Fields = "Fields" if language == "en-us" else "Campos"
                    if action == "tagf":
                        us = f"Invalid or missing mandatory tag: {fields_en[i]}/{fields_pt[i]}"
                        pt = f"Tag inválida ou obrigatória: {fields_en[i]}/{fields_pt[i]}"
                        del recon[session][item][Fields][0][field]
                    else:
                        us = f"Mandatory field: {field}"
                        pt = f"Campo obrigatório: {field}"
                        recon[session][item][Fields][0][field] = ""
                    status, message, reports = corelib.process(recon)
                    if message in [us, pt]: validated = True
                    self.assertEqual(status, False)
                    self.assertEqual(validated, True)
                    status, message = "", ""
                    i += 1
                    
    def mandatory_recon(self):
        recon_en, recon_pt = self.open_recon()
        fields_en = ["Rule"]
        fields_pt = ["Regra"]
        for language in ["en-us", "pt-br"]:
            fields = fields_en if language == "en-us" else fields_pt
            i = 0
            for action in ["tagf", "tagv"]:
                for field in fields:
                    recon = copy.copy(recon_en) if language == "en-us" else copy.copy(recon_pt)
                    session = "Recon" if language == "en-us" else "Conciliação"
                    if action == "tagf":
                        us = f"Invalid or missing mandatory tag: {fields_en[i]}/{fields_pt[i]}"
                        pt = f"Tag inválida ou obrigatória: {fields_en[i]}/{fields_pt[i]}"
                        del recon[session][0][field]
                    else:
                        us = f"Mandatory field: {field}"
                        pt = f"Campo obrigatório: {field}"
                        recon[session][0][field] = ""
                    status, message, reports = corelib.process(recon)
                    if message in [us, pt]: validated = True
                    self.assertEqual(status, False)
                    self.assertEqual(validated, True)
                    status, message = "", ""
                    i += 1                    
                   
    def mandatory_recon_field(self):
        recon_en, recon_pt = self.open_recon()
        fields_en = ["Type", "Name"]
        fields_pt = ["Tipo", "Nome"]
        item = 0
        for language in ["en-us", "pt-br"]:
            fields = fields_en if language == "en-us" else fields_pt
            i = 0
            for action in ["tagf", "tagv"]:
                for field in fields:
                    recon = copy.copy(recon_en) if language == "en-us" else copy.copy(recon_pt)
                    session = "Recon" if language == "en-us" else "Conciliação"
                    Fields = "Fields" if language == "en-us" else "Campos"                    
                    if action == "tagf":
                        us = f"Invalid or missing mandatory tag: {fields_en[i]}/{fields_pt[i]}"
                        pt = f"Tag inválida ou obrigatória: {fields_en[i]}/{fields_pt[i]}"
                        del recon[session][item][Fields][0][field]
                    else:
                        us = f"Mandatory field: {field}"
                        pt = f"Campo obrigatório: {field}"
                        recon[session][item][Fields][0][field] = ""
                    status, message, reports = corelib.process(recon)
                    if message in [us, pt]: validated = True
                    self.assertEqual(status, False)
                    self.assertEqual(validated, True)
                    status, message = "", ""
                    i += 1
                   
    def setUp(self):
        pass
                    
    def test_validate_mandatory(self):
        self.mandatory_info()
        self.mandatory_datasource()
        self.mandatory_datasource_fields()
        self.mandatory_recon()
        self.mandatory_recon_field()

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()