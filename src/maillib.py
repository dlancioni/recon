import os
import logging
import smtplib
from email.message import EmailMessage
from src.fslib import FsLib

fslib = FsLib()

class MailLib:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def send(self, to, subject, message):
        sent = False
        path = fslib.get_path_config("mail.cfg")
        info = fslib.open_json(path)
        server = info["smtp"]
        from_mail = info["from"]
        password = info["password"]
        if password == "":
            return False
        try:
            msg = EmailMessage()
            msg["Subject"] = subject
            msg["From"] = from_mail
            msg["To"] = ", ".join(to)
            msg.set_content(message)
            server = smtplib.SMTP(server)
            server.set_debuglevel(1)
            server.starttls()
            server.login(from_mail, password)
            server.send_message(msg)
            server.quit()
            sent = True
        except BaseException as err:
            cat = msglib.get("E6")
            msg = f"{cat} {str(err)}"
            loglib.log(loglib.ERROR, msg)
            sent = False
        return sent