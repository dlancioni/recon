import os
import json
import pathlib

class FsLib:

    def get_dir_parent(self, path):
        return os.path.dirname(path)

    def get_dir_etc(self, file=""):
        path = os.path.abspath(".")        
        path = (path + "\\etc\\") if path.find("\\recon") >= 0 else (path + "\\recon\\etc\\")
        if (file): path += file
        return path

    def get_json(self, path):
        with open(path) as f:
            data = json.load(f)
            return data
        