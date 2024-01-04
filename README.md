# recon
Reconciliation application    

# dependences
Microsoft SQL Server driver      
https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16#download-for-windows      

## Build
Clone repository   
Make sure you have vs build tools updated otherwise sqlite related libs does not compile   
Do not use c:\temp to clone as the build creates the project there   
Add pyinstaller folder to the path   
run pip install -r requirements.txt   
run build.py to create the exe - output is c:\temp\recon   

## Setup
open file setup.json
    define the log path
    

    
