import os
import logging
import pyodbc 
import psycopg2
import sqlite3
import mysql.connector
from sqlite3 import Error
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

    def get_connection(self, path_temp, debug=0, recon_name=""):
        conn = None
        if debug == 0:
            conn = sqlite3.connect(":memory:")
        else:
            connection = fslib.join(path_temp, f"{recon_name}.db")
            conn = sqlite3.connect(connection)
        conn.isolation_level = None
        return conn
    
    def get_data(self, conector, query):
        path = fslib.get_path_config(conector)
        info = fslib.open_json(path)
        if info["db"] == "mysql":
            cn = self.get_connection_mysql(conector)
        if info["db"] == "pgsql":
            cn = self.get_connection_pgsql(conector)
        if info["db"] == "mssql":
            cn = self.get_connection_mssql(conector)            
        cursor = cn.cursor()
        cursor.execute(query)
        rs = cursor.fetchall()
        return rs

    def get_connection_mysql(self, conector):
        path = fslib.get_path_config(conector)
        info = fslib.open_json(path)
        host = info["hostname"]
        db = info["database"]      
        user = info["username"]
        pwd = info["password"]
        cn = mysql.connector.connect(host=host, database=db, user=user, password=pwd)
        return cn
    
    def get_connection_pgsql(self, conector):
        path = fslib.get_path_config(conector)
        info = fslib.open_json(path)
        host = info["hostname"]
        db = info["database"]      
        user = info["username"]
        pwd = info["password"]
        cn = psycopg2.connect(host=host, database=db, user=user, password=pwd)
        return cn
    
    def get_connection_mssql(self, conector):
        path = fslib.get_path_config(conector)
        info = fslib.open_json(path)
        driver = "{ODBC Driver 18 for SQL Server}"
        host = info["hostname"]
        db = info["database"]
        user = info["username"]
        pwd = info["password"]
        connection = f"Driver={driver}; Server={host}; Database={db}; UID={user}; PWD={pwd}; TrustServerCertificate=Yes"
        cn = pyodbc.connect(connection)
        return cn
    
    


