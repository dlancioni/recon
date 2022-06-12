import os
import json
os.system("cls")

class CoreLib:
    
    def main(self):
        with open("c:\\temp\\dictionary.txt") as f:
            data = f.read()   
        data = json.loads(data)
        print(data)
        
