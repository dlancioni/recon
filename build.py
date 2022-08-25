"""
Author: David Lancioni
Target: Build app to be distributed 
How to use: just hit F5 :)
"""
import os 
import shutil 
import subprocess
from os.path import exists
from src.fslib import FsLib
fslib = FsLib()

# run pyinstaller
os.system("cls || clear")
path = fslib.join(fslib.get_path(), "main.py") 
command = "pyinstaller.exe --onefile --icon=icon.ico --name recon " + path
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
process.wait()
print(process.returncode) 
os.system("cls || clear")

# base paths
source = fslib.get_path()
target = "c:\\temp\\recon"

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

# copy folder structure
print(f"Copying folders to {target}")
dirs = ["config", "data", "logs", "reports", "task"]
for dir in dirs:
    path1 = fslib.join(source, dir)
    path2 = fslib.join(target, dir)
    if exists(path2):
        shutil.rmtree(path2)
    shutil.copytree(path1, path2)
    print(f"{path1}")
    
# delete configs used in dev only
print(f"Deleting recons used for test")
path = fslib.join(target, "task")
files = os.listdir(path)
for file in files:
    if str(file).find("test") >= 0:
        path1 = fslib.join(path, file)
        if fslib.is_file(path1):
            os.remove(path1)

# delete logs and reports
print(f"Deleting logs and reports")
for directory in ["logs", "reports", "data"]:
    path = fslib.join(target, directory)
    files = os.listdir(path)
    for file in files:
        path1 = fslib.join(path, file)
        if fslib.is_file(path1):
            if str(file) != "Saldo.txt" and str(file) != "Extrato.txt":
                os.remove(path1)

print(f"[SUCCESS] To run the app visit: {target}")