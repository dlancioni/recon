import os
import sys
import csv
import click
import logging
import argparse
from datetime import timedelta
from timeit import default_timer as timer
from termcolor import colored, cprint
from src.fslib import FsLib
from src.msglib import MsgLib
from src.utillib import UtilLib
from src.corelib import CoreLib
from src.reportlib import ReportLib

""" general declaration """
fslib = FsLib()
msglib = MsgLib()
utillib = UtilLib()
corelib = CoreLib()
reportlib = ReportLib()
utillib.cls()

""" control input flow """
@click.command()
@click.option('--f',  help=f"{msglib.get('M12')}", default="recon.cfg")
@click.option('--c',  help=f"{msglib.get('M13')}", is_flag=True)
@click.option('--t',  help=f"{msglib.get('M14')}", is_flag=True)
@click.option('--rs', help=f"{msglib.get('M15')}", is_flag=True)
@click.option('--ra', help=f"{msglib.get('M16')}", is_flag=True)
@click.option('--s',  help=f"{msglib.get('M17')}", default=0)

def main(f, c, t, rs, ra, s):
    
    """ Process the conciliation """
    start = timer()
    msglib.print(msglib.get("M1"))
    status, error, reports = corelib.process(f)
    end = timer()
    
    """ time elapsed """
    if t == True:
        msg = msglib.get("M3")
        msg = msglib.set_time(f"{msg}: {timedelta(seconds=end-start)}")
        msg = colored(msg, "yellow")
        print(msg)
        
    """ all done """
    msglib.print(msglib.get("M2"))
    
    """ generate reports """
    if status == True:
        if c == True:
            utillib.cls()
        if rs in [1, 2, 12]:
            reportlib.print_report(1, reports[0], s)
        if ra in [1, 2, 12]:
            reportlib.print_report(2, reports[1], s)

if __name__ == '__main__':
    main()