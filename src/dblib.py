import os
import logging
import sqlite3
from sqlite3 import Error
from prettytable import from_db_cursor
from src.utillib import UtilLib

utillib = UtilLib()

class DbLib:
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def get_connection(db=""):
        conn = None
        #conn = sqlite3.connect(":memory:")
        conn = sqlite3.connect("c:\\temp\\db.db")
        conn.isolation_level = None
        return conn        
    
    def query(self, cn, sql, format=False):
        cn.execute(sql)
        if format == False:
            rs = cn.fetchall()
        if format == True:
            rs = from_db_cursor(cn)
        return rs
    
    def execute(self, cn, sql):
        rows_affected = 0
        self.method = "dblib.execute()"
        try:
            cn.execute(sql)
            rows_affected = cn.rowcount
        except Error as err:
            message = f"{self.method}: SQL Error -> {str(err)}"
            utillib.log(message)
            raise Exception(message)
    
    def begin_tran(self):
        self.method = "dblib.begin_tran()"
        cn = self.get_connection()
        cursor = cn.cursor()
        #cursor.execute("begin")
        return cursor
    
    def commit_tran(self, cn):
        self.method = "dblib.commit_tran()"
        #cn.execute("commit")
        
    def rollback_tran(self, cn):
        self.method = "dblib.rollback_tran()"
        #cn.execute("rollback")