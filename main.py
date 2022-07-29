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
@click.option('--fn', prompt=f"{msglib.get('M12')}", help=f"help", default="recon [pt-br].cfg")
@click.option('--cs',  prompt=f"{msglib.get('M13')}", help=f"help", default=0)
@click.option('--et',  prompt=f"{msglib.get('M14')}", help=f"help", default=0)
@click.option('--rs', prompt=f"{msglib.get('M15')}", help=f"help", default=12)
@click.option('--ra', prompt=f"{msglib.get('M16')}", help=f"help", default=0)

def main(fn, cs, et, rs, ra):

    """ Process the conciliation """
    start = timer()
    msglib.print(msglib.get("M1"))
    status, error, reports = corelib.process(fn)
    end = timer()

    """ time elapsed """
    if et:
        msg = msglib.get("M3")
        msg = msglib.set_time(f"{msg}: {timedelta(seconds=end-start)}")
        msg = colored(msg, "yellow")
        print(msg)

    """ present results in screen """
    if status == True:
        print(colored(msglib.set_time(msglib.get("M10", [fn])), "green"))
    else:
        print(colored(msglib.set_time(msglib.get("M11", [fn])), "red"))
        print(colored(msglib.set_time(error), "red"))

    """ all done """
    msglib.print(msglib.get("M2"))

    """ generate reports """
    if status == True:
        if rs in [1, 2, 12]:
            reportlib.print_report(1, reports[0], rs)
        if ra in [1, 2, 12]:
            reportlib.print_report(2, reports[1], ra)

if __name__ == '__main__':
    main()