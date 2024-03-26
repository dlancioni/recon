# Recon
Reconciliation application    

# Dependences
Microsoft SQL Server driver      
https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16#download-for-windows

PYInstaller
Library used to compile (or build) the application. Go to the command prompt and run a search like dir /s *pyinstaller* to find where the .exe file is located, keep the path and append it to the "Path" section of your envorment variables.

Build Tools
CPP related library for windows used to compile sqlite on the fly (unfortuntelly).

## Build
Clone repository   
run pip install -r requirements.txt   
run build.py to create the binaries - output in build an dist folders inside the project
The configuration files and folders will be copied there as well with default options.
See launch.json to execute the recons.

## Setup
open file setup.json
    define the log path
    

## Reconciliation file
Id: Unique reconciliation id
Nome: Unique name
Descrição: Brief description about the reconciliation
Results: [All] Display all fields imported in the output results (better to see divergences)
         [Difference] Display fields with differences only 
