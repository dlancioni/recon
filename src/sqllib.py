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
    
    def get_field_list(self, fields=[], types=None, funcs=None):
        i = 0
        sql = ""
        if fields == []: return ""
        size = len(fields) -1
        while i <= size:
            name = fields[i]
            type = types[i] if types != None else ""
            func = funcs[i] if funcs != None else ""
            sql += f"{func}({name}) {name}, " if func else f"{name}, "
            i += 1
        sql = sql.strip()[:-1]
        sql = sql.lower()
        return sql
    
    def get_value_list(self, fields, types, values, masks):
        i = 0
        sql = ""        
        if fields == None or types== None or values == None: return ""
        size = len(fields) -1
        while i <= size:
            name = fields[i]
            type = types[i] if types != None else ""
            quote = "'" if type in ["text", "datetime"] else ""
            value = str(values[i]).strip()
            mask = str(masks[i]).strip()
            if mask == ",": 
                value = value.replace(".", "").replace(",", ".")
            sql += f"{quote}{value}{quote}, "
            i += 1
        sql = sql.strip()[:-1]
        return sql
    
    def get_create_table_definition(self, tablename, fields, types):
        i = 0
        sql = ""
        fieldlist = "id integer, id_parent integer, recon text, rule text, "
        if tablename == "" or fields == "" or types == "": return ""
        size = len(fields) -1
        while i <= size:
            name = str(fields[i]).strip()
            type = str(types[i]).strip()
            type = self.get_field_type(type)
            fieldlist += f"{name} {type}, "
            i += 1
        fieldlist = fieldlist[:-2]
        sql = f"create table {tablename} ({fieldlist})"
        return sql
    
    def get_create_index_definition(self, tablename, fields):
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
    
    def get_sql_insert(self, tablename, fields, values):
        sql = ""
        if tablename == "" or fields == "" or values == "": return ""
        sql = f"insert into {tablename} ({fields}) values ({values})"
        return sql
    
    def get_table_structure(self, f1, t1, f2, t2):
        if len(f1) != len(t1) or len(f2) != len(t2): return [],[]
        f = list(dict.fromkeys(f1 + f2))
        t = list(dict.fromkeys(t1 + t2))
        return f, t    