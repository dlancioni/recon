import os

class UtilLib:

    def __init__(self):
        pass
    
    def print(self, cursor):
        os.system("cls")
        for side in range(1,3):
            print(f"Side{side}:")
            cursor.execute(f"select * from tmp1{side}")
            rows = cursor.fetchall()
            for row in rows:
                print(row)