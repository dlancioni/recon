# Recon
Reconciliation application    

# Dependences   
Microsoft SQL Server driver      
https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16#download-for-windows

PYInstaller   
Library used to compile (or build) the application, after creating the venv copy the path for pyinstaller.exe and paste in the build.py file (see line 15).

## Build   
Clone repository      
Open the project using vs code and create the virtual environment. 
Make sure build.py is pointing the to right pyinstaller.exe as per above note.
Run build.py to create the binaries - output in build an dist folders inside the project.
The configuration files and folders will be copied there as well with default options.
See launch.json to execute the recons.   

## Setup   
open file setup.json   
    define the log path       

## Reconciliation file   
Id: Unique reconciliation id   
Nome: Unique name
Email: Email to send notifications about the reconciliation result (success or fail). Either value or tag are not mandatory and once not informed emails are not send out.  
Description: Brief description about the reconciliation   
Results: [All] Display all fields imported in the output results (better to see divergences)   
         [Difference] Display fields with differences only    
