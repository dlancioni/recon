import os
import sys
import json
import pathlib

class FsLib:

    def get_path(self):
        """ root or application path, where the .exe lives """
        if getattr(sys, 'frozen', False):
            path = os.path.dirname(sys.executable)
        elif __file__:
            path = os.path.dirname(__file__)
            for dir in ["\src", "\\src", "/src"]:
                path = path.replace(dir, "")
        return path

    def get_path_etc(self, file=""):
        path = self.get_path()
        path = os.path.join(path, "etc")
        return path
    
    def get_path_config(self, file=""):
        path = self.get_path()
        path = os.path.join(path, "config")
        return path
    
    def get_path_log(self, file=""):
        path = self.get_path()
        path = os.path.join(path, "log")
        return path
    
    def get_path_file(self, file=""):
        path = self.get_path()
        path = os.path.join(path, "file")
        return path

    def get_json(self, path):
        with open(path) as f:
            data = json.load(f)
            return data
        
    def get_dir_parent(self, path):
        return os.path.dirname(path)        