import datetime
import os
import pendulum

class UtilLib:

    def __init__(self):
        pass
    
    def diff(self, arr):
        seen = set()
        arr = list(arr)
        diff = [x for x in arr if x in seen or seen.add(x)]
        return list(diff)
    
    def remove_dup(self, arr):
        return list(dict.fromkeys(arr))

    def cls(self):
        os.system("cls||clear")        
        
    def expire(self):      
        year = str(pendulum.now().format("YYYY")).strip()
        valid = (year == "2022")
        return valid
    
    def apply_date_pattern(filename):
        dt = datetime.today()
        yyyy = dt.strftime('%Y')                #YYYY
        yy = dt.strftime('%y')                  #YY
        mmm = dt.strftime('%b')                 #MMM
        mm = dt.strftime('%m')                  #MM
        dd = dt.strftime('%d')                  #DD
        filename = filename.lower()
        filename = filename.replace("<yyyy>", yyyy)
        filename = filename.replace("<yy>", yy)
        filename = filename.replace("<mmm>", yy)
        filename = filename.replace("<mm>", mm)
        filename = filename.replace("<dd>", dd)
        return filename