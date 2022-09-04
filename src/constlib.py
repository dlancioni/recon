from pconst import const

# Recon info
const.SIDES = ["1", "2"]
const.STATUS_MATCHED = 1
const.STATUS_DIVERGENT = 2
const.STATUS_ORPHAN = 3

const.FIELD_ID = "_id"
const.FIELD_SIDE = "_side"
const.FIELD_ID_PARENT = "_id_parent"
const.FIELD_RECON = "_recon"
const.FIELD_RULE = "_rule"
const.FIELD_ID_STATUS = "_id_status"
const.FIELD_STATUS = "_status"
const.MATCH_TYPE_KEY = ["key", "chave"]
const.MATCH_TYPE_COMPARE = ["compare", "comparar"]

# Datasource info
const.DATASOURCES = ["Api", "Custom", "Db", "Delimited", "Delimitado", "Excel", "Positional", "Posicional"]
const.DATASOURCE_API = ["Api"]
const.DATASOURCE_CUSTOM = ["Custom"]
const.DATASOURCE_DB = ["Db"]
const.DATASOURCE_DELIMITED = ["Delimited", "Delimitado"]
const.DATASOURCE_POSITIONAL = ["Positional", "Posicional"]
const.DATASOURCE_EXCEL = ["Excel"]

# Data types
const.DATATYPE = ["integer", "decimal", "text", "datetime"] + ["inteiro", "texto", "datahora"]
const.DATATYPE_NUMERIC = ["integer", "decimal"] + ["inteiro"]
const.DATATYPE_DATETIME = ["datetime", "datahora"]
const.DATATYPE_DECIMAL = ["decimal"]