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
from src.constlib import const

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
            "Results":"Resultados",
            "Datasources":"Dados",
            "Fields":"Campos",
            "Side":"Lado",
            "Path":"Caminho",
            "File":"Arquivo",
            "Position":"Posição",
            "Size":"Tamanho",            
            "Delimiter":"Delimitador",
            "Start":"Inicio",
            "Type":"Tipo",
            "Value":"Valor",
            "Mask":"Mascara",
            "Recon":"Conciliação",
            "Rule":"Regra",
            "Tolerance":"Tolerancia",
            "Type":"Tipo",
            "Function":"Função",
            "Default Value":"Valor Padrão",
            "Operator":"Operador",
            "Connector":"Conector",
            "Query":"Consulta",
            "Sheet":"Planilha"
        }
        return tags

    def open_recon(self, recon):
        loglib = LogLib("Setuplib", "open_recon")
        msg = ""
        if type(recon) == dict:
            return recon
        else:
            try:
                path = fslib.get_path_task()
                if fslib.is_dir(path) == False:
                    raise Exception(msglib.get("V17", [path]))
                filename = str(recon.split(".")[0]) +".cfg"
                filename = fslib.join(path, filename)
                if fslib.is_file(filename) == False:
                    raise Exception(msglib.get("V4", [filename]))
                recon = fslib.open_json(filename)
            except json.decoder.JSONDecodeError as err:
                cat = msglib.get("E4")
                error = msglib.get("E5", [err.lineno, err.colno, err.msg])
                msg = f"{cat} {str(error)}"
                loglib.log(loglib.ERROR, msg)
                raise Exception(msg)
            except BaseException as err:
                raise
        return recon

    def tagfv(self, doc, tag_en):
        f, v = "", ""
        tag_pt = self.translate(tag_en)
        tag_en = tag_en.title().strip()
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
                tag_pt = self.translate(tag_en)
                msg = f"{tag_en}/{tag_pt}"
                msg = msglib.get("V1", [msg])
                raise Exception(msg)
        return f

    def tag_value(self, doc, tag_en="", mandatory=True):
        f, v = self.tagfv(doc, tag_en)
        return v

    def translate(self, tag_en=""):
        tag_pt = ""
        tag_en = tag_en.title()
        tags = self.tag_def()
        tag_pt = tags[tag_en]
        if tag_pt.strip() == "":
            raise Exception("tag_pt not found in setuplib.translate()")
        return tag_pt

            
