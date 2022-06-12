import os
import json
os.system("cls")

data =  {
    "Id": 1,
    "Name": "Saldos",
    "Source":
    {
        "Name": "Sybase 1",
        "Table": "tb_balance",
        "Key": ["account"],
        "Field": ["account", "balance"],
        "Type": ["text", "decimal"],
        "Mask": ["", ""]
    },
    "Target":
    {
        "Name": "Sybase 1",
        "Table": "tb_statement",
        "Key": ["account"],
        "Field": ["date", "account", "balance"],
        "Type": ["datetime", "text", "decimal"],
        "Mask": ["", ""]
    }
}
