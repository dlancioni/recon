import os
import pendulum
from src.msglib import MsgLib

msglib = MsgLib()

class ExpireLib:

    def __init__(self):
        pass
        
    def expired(self):
        expire_at = "2024"
        year = str(pendulum.now().format("YYYY")).strip()
        expired = (year == expire_at)
        if expired == True:
            msg = msglib.get("M18")
            print(msg)
        return expired