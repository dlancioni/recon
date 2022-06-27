import os

class UtilLib:

    def __init__(self):
        pass
    
    def print(self, cursor):
        for side in range(1,3):
            print(f"Side{side}:")
            cursor.execute(f"select * from tmp1{side}")
            rows = cursor.fetchall()
            for row in rows:
                print(row)
                
    def log(self, message):
        import time
        from datetime import datetime
        now = datetime.now()
        dt = str(time.strftime("%Y-%m-%d %H:%M:%S", now.timetuple()))
        output = f"{dt}: {message}"
        print(output)
        
    def query(self, cursor, sql):
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            print(row)        