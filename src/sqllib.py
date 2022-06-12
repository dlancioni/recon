class SqlLib:

    # field type used to create table
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
    
    # field list to generate select, group by, order by
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
        return sql
    
    # value list to generate insert
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
    
    # generate script to create table
    def get_create_table_definition(self, tablename, fields, types):
        i = 0
        sql = ""
        fieldlist = "";
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
    
    # generate script to create index
    def get_create_index_definition(self, tablename, fields):
        i = 0
        sql = ""
        fieldlist = "";
        if tablename == "" or fields == "": return ""
        size = len(fields) -1
        while i <= size:
            name = str(fields[i]).strip()
            fieldlist += f"{name}, "
            i += 1
        fieldlist = fieldlist[:-2]
        sql = f"create index idx_{tablename} on {tablename} ({fieldlist})"
        return sql    