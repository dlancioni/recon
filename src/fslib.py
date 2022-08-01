import os
import sys
import json
import pathlib
import csv

class FsLib:

    def open_json(self, path):
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
            return data

    def get_csv_as_list(self, path, delimiter=";"):
        with open(path, encoding="utf-8") as f:
            data = csv.reader(f, delimiter=delimiter)
            data = list(data)
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
        path = self.join(self.get_path(), "recons") if path == "" else path
        path = self.join(path, file)
        return path
        
    def get_path_log(self, path="", file=""):
        if path == "":
            path = self.get_path()
            path = self.join(path, "logs")
        path = self.join(path, file)
        return path

    def get_path_file(self, path="", file=""):
        path = self.join(self.get_path(), "data") if path == "" else path
        path = self.join(path, file)
        return path
    
    def get_path_report(self, path="", file=""):
        path = self.join(self.get_path(), "reports") if path == "" else path
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

    def is_dir(self, path):
        if not os.path.isdir(path):
            return False
        else:
            return True
        
    def is_file(self, filename):
        if not os.path.exists(filename):
            return False
        else:
            return True