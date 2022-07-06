# https://www.sqlitetutorial.net/sqlite-python/
import os
import logging
import sqlite3
from sqlite3 import Error
from src.utillib import UtilLib

class DbLib:
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def begin_tran(self):
        self.method = "dblib.begin_tran()"
        cn = self.get_connection()
        cursor = cn.cursor()
        cursor.execute("begin")
        self.logger.info(f"{self.method}: Start new database transaction")
        return cursor
    
    def execute(self, cn, sql):
        rows_affected = 0
        self.method = "dblib.execute()"
        utillib = UtilLib()
        try:
            cn.execute(sql)
            rows_affected = cn.rowcount
        except Error as err:
            message = f"{self.method}: SQL Error -> {str(err)}"
            utillib.log(message)
            self.logger.error(message)
        finally:
            self.logger.info(f"SQL Query: {sql}")
            return rows_affected
    
    def commit_tran(self, cn):
        self.method = "dblib.commit_tran()"
        cn.execute("commit")
        self.logger.info(f"{self.method}: Transaction commited")
        
    def rollback_tran(self, cn):
        self.method = "dblib.rollback_tran()"
        cn.execute("rollback")
        self.logger.info(f"{self.method}: Transaction rollback")

    def get_connection(db=""):
        conn = None
        conn = sqlite3.connect(":memory:")
        #conn = sqlite3.connect("c:\\temp\\db.db")
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