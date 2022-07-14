import os
import sys
import json
import pathlib

class FsLib:
    
    def open_json(self, path):
        with open(path) as f:
            data = json.load(f)
            return data    

    def join(self, path1, path2):
        path = os.path.join(path1, path2) if path2.strip() != "" else path1
        return path

    def get_path(self):
        """ root or application path, where the .exe lives """
        if getattr(sys, 'frozen', False):
            path = os.path.dirname(sys.executable)
        elif __file__:
            path = os.path.dirname(__file__)
            for dir in ["\src", "\\src", "/src"]:
                path = path.replace(dir, "")
        return path
    
    def get_path_recon(self, path="", file=""):
        path = self.get_path() if path == "" else path
        path = self.join(path, "recon")
        path = self.join(path, file)
        return path
        
    def get_path_log(self, path="", file=""):
        if path == "":
            path = self.get_path()
            path = self.join(path, "log")
        path = self.join(path, file)
        return path

    def get_path_file(self, path="", file=""):
        path = self.get_path() if path == "" else path
        path = self.join(path, "data")
        path = self.join(path, file)
        return path
    
    def get_path_report(self, path="", file=""):
        path = self.get_path() if path == "" else path
        path = self.join(path, "report")
        path = self.join(path, file)
        return path    

    def get_path_etc(self, file=""):
        path = self.get_path()
        path = self.join(path, "etc")
        path = self.join(path, file)
        return path
    
    def get_path_config(self, file=""):
        path = self.get_path()
        path = self.join(path, "config")
        path = self.join(path, file)
        return path
       
    def get_parent(self, path):
        return os.path.dirname(path)