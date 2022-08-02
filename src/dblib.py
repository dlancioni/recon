import os
import logging
import sqlite3
from sqlite3 import Error
from prettytable import from_db_cursor
from src.fslib import FsLib

fslib = FsLib()

class DbLib:
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def query(self, cn, sql, format=False):
        cn.execute(sql)
        if format == False:
            rs = cn.fetchall()
        if format == True:
            rs = from_db_cursor(cn)
        return rs
    
    def execute(self, cn, sql):
        rows_affected = 0
        cn.execute(sql)
        rows_affected = cn.rowcount
        return rows_affected
    
    def get_connection(self, path_temp, debug=0):
        conn = None
        if debug == 0:
            conn = sqlite3.connect(":memory:")
        else:
            connection = fslib.join(path_temp, "log.db")
            conn = sqlite3.connect(connection)
        conn.isolation_level = None
        return conn

    def begin_tran(self, cn, debug=0):
        cursor = cn.cursor()
        if debug == 0:        
            cursor.execute("begin")
        return cursor
    
    def commit_tran(self, cn, debug=0):
        if debug == 0:        
            cn.execute("commit")
        
    def rollback_tran(self, cn, debug=0):
        if debug == 0:
            cn.execute("rollback")