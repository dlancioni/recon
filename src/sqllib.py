class SqlLib:

    # field type used to create table
    def get_field_type(key=""):
        types = {
            "integer": "Integer",
            "decimal": "Real",
            "text": "Text",
            "datetime": "Text",
        }
        return types.get(key)
    
    # field list to generate select, group by, order by
    def get_field_list(fields=[], types=None, funcs=None):
        i = 0
        sql = ""
        if fields == []: return ""
        size = len(fields) -1
        while i <= size:
            name = fields[i]
            func = funcs[i] if funcs != None else ""
            sql += f"{func}({name}) {name}, " if func else f"{name}, "
            i += 1
        sql = sql.strip()[:-1]    
        return sql    