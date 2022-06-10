import os
import json
os.system("cls")

data =  {
    "Id": 1,
    "Name": "Saldo x Extrato",
    "Side 1":
    {
        "Name": "Balance",
        "Datasource":
        [
            {
                "Name": "Sybase 1",
                "Table": "tb_balance",
                "Key": ["account"],
                "Field": ["account", "balance"],
                "Type": ["text", "decimal"],
                "Aggregation": ["", "sum"],
            }
        ]
    },
    "Side 2":
    {
        "Name": "Statement",
        "Datasource":
        [
            {
                "Name": "Sybase 1",
                "Table": "tb_statement",
                "Key": ["account"],
                "Field": ["date", "account", "balance"],
                "Type": ["datetime", "text", "decimal"],
                "Aggregation": ["", "", "sum"],
            }
        ]
    }
}

# navigate the dict
print( data["Side 1"]["Datasource"][0]["Name"] )

# check tag exists
print( "Side 1" in data )
print( "Field" in data["Side 2"]["Datasource"][0] )

# size
print(len(data["Side 1"]["Datasource"]))

# iterate
for datasource in data["Side 1"]["Datasource"]:
    for field in datasource["Field"]:
        print(field)
 
    