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
from src.expirelib import ExpireLib
from src.constlib import const

""" general declaration """
fslib = FsLib()
msglib = MsgLib()
utillib = UtilLib()
corelib = CoreLib()
reportlib = ReportLib()
expirelib = ExpireLib()
utillib.cls()

""" control input flow """
@click.command()
@click.option('-f',  help=f"{msglib.get('M12')}", default="recon.cfg")
@click.option('-c',  help=f"{msglib.get('M13')}", is_flag=True)
@click.option('-t',  help=f"{msglib.get('M14')}", is_flag=True)
@click.option('-rs', help=f"{msglib.get('M15')}", is_flag=True)
@click.option('-ra', help=f"{msglib.get('M16')}", is_flag=True)
@click.option('-s',  help=f"{msglib.get('M17')}", default=0)
@click.option('-v',  help=f"{msglib.get('M19')}", is_flag=True)

def main(f, c, t, rs, ra, s, v):

    """ Process the conciliation """
    if v == True:
        print(msglib.get("M29") + expirelib.get_version())
        return

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
    
    """ print reports """
    if status == True:
        if c == True:
            utillib.cls()
        if rs in [1, 2, 12]:
            reportlib.print_report(1, reports[const.REPORT_SYNTHETIC], s)
        if ra in [1, 2, 12]:
            reportlib.print_report(2, reports[const.REPORT_ANALYTIC], s)

if __name__ == '__main__':
    if expirelib.expired() == False:
        main()