import os
import logging
import smtplib
from src.fslib import FsLib
from src.msglib import MsgLib
from src.setuplib import SetupLib
from email.message import EmailMessage

fslib = FsLib()
msglib = MsgLib()
setuplib = SetupLib()

class MailLib:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def send_mail(self, to, subject, message):
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
            msg["To"] = to
            msg.set_content(message)
            server = smtplib.SMTP(server)
            #server.set_debuglevel(1)
            server.starttls()
            server.login(from_mail, password)
            server.send_message(msg)
            server.quit()
            sent = True
        except BaseException as err:
            cat = msglib.get("E6")
            msg = f"{cat} {str(err)}"
            sent = False
        return sent
    
    def notify_success(self, recon):
        to = setuplib.tag_value(recon, "Email")        
        if to.strip() != "":
            name = setuplib.tag_value(recon, "Name")
            subject = msglib.get("M21", [name])
            body = msglib.get("M23")
            self.send_mail(to, subject, body)

    def notify_fail(self, recon, message):
        to = setuplib.tag_value(recon, "Email")
        if to.strip() != "":
            name = setuplib.tag_value(recon, "Name")
            subject = msglib.get("M22", [name])
            body = message
            self.send_mail(to, subject, body)