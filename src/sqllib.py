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
    
    def get_field_list(self, fields=[], types=[], funcs=[]):
        i = 0
        sql = ""
        if fields == []: return ""
        size = len(fields) -1
        while i <= size:
            name = fields[i]
            type = types[i] if types != [] else ""
            func = funcs[i] if funcs != [] else ""
            sql += f"{func}({name}) {name}, " if func else f"{name}, "
            i += 1
        sql = sql.strip()[:-1]
        sql = sql.lower()
        return sql
    
    def get_value_list(self, fields=[], types=[], values=[], masks=[]):
        i = 0
        sql = ""        
        if fields == [] or types== [] or values == []: return ""
        size = len(fields) -1
        while i <= size:
            name = fields[i]
            type = types[i] if types != [] else ""
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
        fieldlist = ""
        fieldlist += "id integer primary key"
        fieldlist += ", id_parent integer default 0"
        fieldlist += ", recon text default ''"
        fieldlist += ", rule text default '', "
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

    def get_grouping_list(self, fields=[], funcs=[]):
        i = 0
        sql = ""
        if fields == "" or funcs == "": return ""
        size = len(fields) -1
        while i <= size:
            name = fields[i]
            func = funcs[i]
            sql += f"{name}, " if not func else ""
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