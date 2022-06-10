import os
import json
os.system("cls")

class Main:
    def main(self):
        # reading the data from file
        with open("c:\\temp\\dictionary.txt") as f:
            data = f.read()
        data = json.loads(data)    


    
