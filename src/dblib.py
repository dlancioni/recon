# https://www.sqlitetutorial.net/sqlite-python/
import os
import sqlite3
from sqlite3 import Error

class Db:

    def get_connection(db=""):
        conn = None
        conn = sqlite3.connect(":memory:")
        conn.isolation_level = None
        return conn

    def create_connection(db_file):
        conn = None
        try:
            # Get Connection
            conn = sqlite3.connect(db_file)
            conn.isolation_level = None

            # Create table
            cursor = conn.cursor()
            cursor.execute("create table if not exists tb_1 (id integer, name text)")

            # Insert data
            cursor = conn.cursor()
            cursor.execute("begin")
            cursor.execute("insert into tb_1 (id, name) values (1, 'David')")
            cursor.execute("insert into tb_1 (id, name) values (2, 'Renata')")
            cursor.execute("commit")
            print(cursor.lastrowid) # Print 2 (note it is not identity)

            # Select data
            cursor = conn.cursor()
            cursor.execute("SELECT id, name from tb_1 where id = ?", (2,))
            rows = cursor.fetchall()

            # Field names
            print(cursor.description[0][0]) # id
            print(cursor.description[0][1]) # name        

            # Field values
            for row in rows:
                print(str(row[0]) + " " + row[1])

        except Error as e:
            cursor.execute("rollback")
            print(e)
        finally:
            if conn:
                conn.close()