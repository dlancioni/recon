class EtlLib:

    def __init__(self):
        pass
    
    def import_file(self):
        with open("c:\\temp\\dictionary.txt") as f:
            data = f.read()
        data = json.loads(data)
        print(data)