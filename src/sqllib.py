class SqlLib:
    
    def __init__(self):
        pass    

    def get_field_type(self, key=""):
        types = {
            "integer": "integer",
            "decimal": "real",
            "text": "text",
            "datetime": "text",
        }
        key = types.get(key.lower())
        key = "" if key is None else key
        return key
    
    def get_field_list(self, field_def=""):
        i = 0
        sql = ""
        if field_def == "": return ""
        size = len(field_def) -1
        while i <= size:
            name = field_def[i]["name"]
            type = field_def[i]["type"]
            function = field_def[i]["function"] if "function" in field_def[i] else ""
            sql += f"{function}({name}) {name}, " if function else f"{name}, "
            i += 1
        sql = sql.strip()[:-1]
        sql = sql.lower()
        return sql
    
    def get_value_list(self, field_def=""):
        i = 0
        sql = ""        
        if field_def == "": return ""
        size = len(field_def) -1
        while i <= size:
            name = field_def[i]["name"]
            type = field_def[i]["type"] if "type" in field_def[i] else ""
            value = str(field_def[i]["value"]).strip() if "value" in field_def[i] else ""
            mask = str(field_def[i]["mask"]).strip() if "mask" in field_def[i] else ""
            quote = "'" if type in ["text", "datetime"] else ""
            if mask == ",":
                value = value.replace(".", "").replace(",", ".")
            sql += f"{quote}{value}{quote}, "
            i += 1
        sql = sql.strip()[:-1]
        return sql
    
    def get_create_table_definition(self, tablename, fields, types):
        i = 0
        sql = ""
        fieldlist = ""
        fieldlist += "id integer primary key"
        fieldlist += ", id_parent integer default 0"
        fieldlist += ", recon text default ''"
        fieldlist += ", rule text default ''"
        fieldlist += ", status text default 'orphan'"
        fieldlist += ", "
        if tablename == "" or fields == [] or types == []: return ""
        size = len(fields) -1
        while i <= size:
            name = str(fields[i]).strip()
            type = str(types[i]).strip()
            type = self.get_field_type(type)
            fieldlist += f"{name} {type}, "
            i += 1
        fieldlist = fieldlist[:-2]
        sql = f"create table {tablename} ({fieldlist})"
        return sql.lower()
    
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

    def get_grouping_list(self, field_def=""):
        i = 0
        sql = ""
        if field_def == "": return ""
        size = len(field_def) -1
        while i <= size:
            name = field_def[i]["name"]
            function = field_def[i]["function"] if "function" in field_def[i] else ""
            sql += f"{name}, " if not function else ""
            i += 1
        sql = sql.strip()[:-1]
        sql = sql.lower()
        return sql

    def get_sql_key(self, tb1="", tb2="", fields=""):
        sql = ""
        for field in fields:
            sql += f"and {tb1}.{field} = {tb2}.{field} "
        sql = sql.strip().lower()   
        return sql