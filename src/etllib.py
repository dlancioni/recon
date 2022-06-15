import logging
from sqllib import SqlLib

class EtlLib:

    def __init__(self):
        self.method = "EtlLib.import_file()"
        self.logger = logging.getLogger(__name__)

    def import_file(self, cn, ds):
        self.logger.info(f"{self.method}: Start reading information")
        
        sqlib = SqlLib()
        path = ds["Name"]
        separator = ds["Separator"]
        fields = ds["Field"]
        types = ds["Type"]
        first = True
        with open(path, "r") as file:
            for line in file.readlines():
                if not first:
                    values = line.split(separator)
                    if len(fields) == len(values):
                        for k, v in enumerate(fields):
                            print(fields[k])
                            print(types[k])
                            print(values[k])
                first = False