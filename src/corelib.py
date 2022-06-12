import os
import json
os.system("cls")

class CoreLib:
    
    def main(self):
        with open("c:\\temp\\dictionary.txt") as f:
            data = f.read()   
        data = json.loads(data)
        print(data)

    # merge both field and type lists        
    def get_table_structure(self, f1, t1, f2, t2):
        f = list(dict.fromkeys(f1 + f2))
        t = list(dict.fromkeys(t1 + t2))
        return f, t