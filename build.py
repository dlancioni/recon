"""
Author: David Lancioni
Target: Build app to be distributed
Steps:
    cd recon
    pyinstaller.exe --onefile --icon=icon.ico --name recon main.py
    python build.py
"""
import os 
from os.path import exists
import shutil 
from src.fslib import FsLib
fslib = FsLib()

os.system("cls || clear")

# base paths
target = "c:\\temp\\recon"
source = fslib.get_path()

# create folder
print(f"Create application folder {target}")
if exists(target):
    shutil.rmtree(target)
os.makedirs(target, mode=0o777, exist_ok=False)

# copy .exe
print(f"Copy recon.exe to {target}")
filename = fslib.join(source, "dist")
filename = fslib.join(filename, "recon.exe")
shutil.copy(filename, target)

print(f"Copying folders to {target}")
dirs = ["config", "file", "log", "recon", "report"]
for dir in dirs:
    path1 = fslib.join(source, dir)
    path2 = fslib.join(target, dir)
    if exists(path2):
        shutil.rmtree(path2)
    shutil.copytree(path1, path2)
    print(f"{path1}")
    
print(f"[SUCCESS] To run the app visit: {target}")