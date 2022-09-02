import os
import pendulum

class ExpireLib:

    def __init__(self):
        pass
        
    def expired(self):
        expire_at = "2023"
        year = str(pendulum.now().format("YYYY")).strip()
        expired = (year == expire_at)
        if expired == True:
            msg = "Essa versao expirou, entre em contato com dlancioni@gmail.com"
            print(msg)
        return expired