from src.baselib import BaseLib
from src.setuplib import SetupLib
from src.constlib import const

setuplib = SetupLib()

class SqlLib(BaseLib):

    def __init__(self):
        pass

    def get_aggregate_function(self, key="", default="Sum"):
        key = "" if key is None else key.lower()
        if key in ["sum", "somar"]:
            return "Sum"
        if key in ["max", "maximo"]:
            return "Max"
        if key in ["min", "minimo"]:
            return "Min"
        if key in ["avg", "media"]:
            return "Avg"
        return default

    def get_field_type(self, key=""):
        key = "" if key is None else key.lower()
        if key in ["integer", "inteiro"]:
            return "Integer"
        if key in ["real", "decimal"]:
            return "Decimal"
        if key in ["text", "texto"]:
            return "Text"
        if key in ["datetime", "datahora"]:
            return "Text"
        return key

    def get_field_list(self, field_def="", aggregation=False):
        i = 0
        sql = ""
        function = ""
        alias = ""
        if field_def == "": return ""
        size = len(field_def) -1        
        while i <= size:
            field_name = setuplib.tag_name(field_def[i], "Name")
            field_type = setuplib.tag_name(field_def[i], "Type")
            datatype = field_def[i]["Datatype"] if "Datatype" in field_def[i] else ""
            name = str(field_def[i][field_name]).strip() if field_name in field_def[i] else ""
            name = f"[{name}]"
            alias = name            
            type = str(field_def[i][field_type]).strip() if field_type in field_def[i] else ""
            decimals = 2
            if aggregation:
                field_function = setuplib.tag_name(field_def[i], "Function", False)
                function = str(field_def[i][field_function]).strip() if field_function in field_def[i] else ""
                if datatype.strip().lower() == "decimal":
                    name = f"Round({name}, {decimals})"
                    if aggregation == True:
                        function = self.get_aggregate_function(function)
            sql += f"{function}({name}) {alias}, " if function else f"{name}, "
            i += 1
        sql = sql.strip()[:-1]
        return sql

    def get_value_list(self, field_def=""):
        i = 0
        sql = ""
        if field_def == "": return ""
        size = len(field_def) -1
        while i <= size:
            field_name = setuplib.tag_name(field_def[i], "Name")
            field_type = setuplib.tag_name(field_def[i], "Type")
            field_value = setuplib.tag_name(field_def[i], "Value")
            field_mask = setuplib.tag_name(field_def[i], "Mask", False)
            name = str(field_def[i][field_name]).strip()
            name = f"[{name}]"
            type = field_def[i][field_type] if field_type in field_def[i] else ""
            value = str(field_def[i][field_value]).strip() if field_value in field_def[i] else ""
            mask = str(field_def[i][field_mask]).strip() if field_mask in field_def[i] else ""
            quote = "'" if type.lower() in ["text", "texto", "datetime", "datahora"] else ""
            if mask == ",":
                value = value.replace(".", "").replace(",", ".")
            sql += f"{quote}{value}{quote}, "
            i += 1
        sql = sql.strip()[:-1]
        return sql
    
    def get_create_table_definition(self, tablename, fields, types, status, side):
        i = 0
        sql = ""
        fieldlist = ""
        fieldlist += f"{const.FIELD_ID} integer primary key, "
        fieldlist += f"{const.FIELD_SIDE} integer default {side}, "
        fieldlist += f"{const.FIELD_ID_PARENT} integer default 0, "
        fieldlist += f"{const.FIELD_RECON} text default '', "
        fieldlist += f"{const.FIELD_RULE} text default '', "
        fieldlist += f"{const.FIELD_ID_STATUS} integer default {const.STATUS_ORPHAN}, "
        fieldlist += f"{const.FIELD_STATUS} text default '{status}', "
        if tablename == "" or fields == [] or types == []: return ""
        size = len(fields) -1
        while i <= size:
            name = str(fields[i]).strip()
            type = str(types[i]).strip()
            type = self.get_field_type(type)
            fieldlist += f"[{name}] {type}, "
            i += 1
        fieldlist = fieldlist[:-2]
        sql = f"create table {tablename} ({fieldlist})"
        return sql
    
    def get_create_index_definition(self, tablename="", fields=""):
        i = 0
        sql = ""
        fieldlist = ""
        if tablename == "" or fields == "": return ""
        size = len(fields) -1
        while i <= size:
            name = str(fields[i]).strip()
            fieldlist += f"{name}, "
            i += 1
        fieldlist = fieldlist[:-2]
        sql = f"create index idx_{tablename} on {tablename} ({fieldlist})"
        return sql
    
    def get_sql_insert(self, tablename="", fields="", values=""):
        sql = ""
        if tablename == "" or fields == "" or values == "": return ""
        sql = f"insert into {tablename} ({fields}) values ({values})"
        return sql
    
    def get_table_structure(self, f1=[], t1=[], f2=[], t2=[]):
        if len(f1) != len(t1) or len(f2) != len(t2): return [],[]
        fields = f1 + f2
        types = []
        fields = list(dict.fromkeys(fields))
        for field in fields:
            if field in f1:
                index = f1.index(field)
                types.append(t1[index])
            elif field in f2:
                index = f2.index(field)
                types.append(t2[index])
        return fields, types

    def get_field_key(self, fields="", tb1="", tb2=""):
        sql = ""
        for field in fields:
            _name = setuplib.tag_name(field, "Name")
            _type = setuplib.tag_name(field, "Type")
            if str(field[_type]).strip().lower() in ["key", "chave"]:
                field_name = "[" + str(field[_name]).strip() + "]"
                sql += f"{field_name}, "
        sql = sql.strip()
        sql = sql[:-1]
        return sql

    def get_sql_key(self, tb1="", tb2="", fields=""):
        sql = ""
        for field in fields:
            _name = setuplib.tag_name(field, "Name")
            _type = setuplib.tag_name(field, "Type")
            if str(field[_type]).strip().lower() in ["key", "chave"]:
                field_name = str(field[_name]).strip()
                field_name = f"[{field_name}]"
                sql += f"and {tb1}.{field_name} = {tb2}.{field_name} "
        sql = sql.strip()
        return sql

    def field_diff(self, field_name, label):
        field_name = str(field_name).replace("[", "")
        field_name = str(field_name).replace("]", "")
        field_name = field_name.strip()
        field_name = field_name + label
        field_name = "[" + field_name + "]"
        return field_name
        