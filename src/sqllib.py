class SqlLib:

    # field type used to create table
    def get_field_type(self, key=""):
        types = {
            "integer": "Integer",
            "decimal": "real",
            "text": "text",
            "datetime": "text",
        }
        key = types.get(key.lower())
        key = "" if key is None else key
        return key
    
    # field list to generate select, group by, order by
    def get_field_list(self, fields=[], types=None, funcs=None, values=None):
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