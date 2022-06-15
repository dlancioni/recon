import logging

class EtlLib:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def import_file(self, cn, ds):
        self.logger.info("Before read the file")        
        path = ds["Name"]
        separator = ds["Separator"]
        with open(path, "r") as file:
            for line in file.readlines():
                values = line.split(separator)
                if len(fields) == len(values):
                    for k, v in enumerate(fields):
                        print(fields[k])
                        print(types[k])
                        print(values[k])
