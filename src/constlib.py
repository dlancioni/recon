from pconst import const

# Recon info
const.SIDES = ["1", "2"]
const.STATUS_MATCHED = 1
const.STATUS_DIVERGENT = 2
const.STATUS_ORPHAN = 3
const.FIELD_ID = "id"
const.FIELD_SIDE = "side"
const.FIELD_ID_PARENT = "id_parent"
const.FIELD_RECON = "recon"
const.FIELD_RULE = "rule"
const.FIELD_ID_STATUS = "id_status"
const.FIELD_STATUS = "status"
const.MATCH_TYPE_KEY = ["Key", "Chave"]
const.MATCH_TYPE_COMPARE = ["Compare", "Comparar"]

# Datasource info
const.DATASOURCES = ["Api", "Db", "Delimited", "Delimitado", "Excel", "Positional", "Posicional"]
const.DATASOURCE_API = ["Api"]
const.DATASOURCE_DB = ["Db"]
const.DATASOURCE_DELIMITED = ["Delimited", "Delimitado"]
const.DATASOURCE_POSITIONAL = ["Positional", "Posicional"]
const.DATASOURCE_EXCEL = ["Excel"]

# Data types
const.DATATYPE = ["integer", "decimal", "text", "datetime"] + ["inteiro", "texto", "datahora"]
const.DATATYPE_NUMERIC = ["integer", "decimal"] + ["inteiro"]