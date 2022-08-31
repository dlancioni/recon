import os

class UtilLib:

    def __init__(self):
        pass
    
    def diff(self, arr):
        seen = set()
        arr = list(arr)
        diff = [x for x in arr if x in seen or seen.add(x)]
        return list(diff)

    def cls(self):
        os.system("cls||clear")