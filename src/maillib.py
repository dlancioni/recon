import os
import csv
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders

from src.fslib import FsLib
from src.msglib import MsgLib
from src.setuplib import SetupLib
from email.message import EmailMessage
from src.constlib import const

fslib = FsLib()
msglib = MsgLib()
setuplib = SetupLib()

class MailLib:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def send_mail(self, to, subject, message, attachments=""):
        sent = False
        path = fslib.get_path_config("mail.cfg")
        info = fslib.open_json(path)
        server = info["smtp"]
        from_mail = info["from"]
        password = info["password"]
        if password == "":
            print("Password not informed for email")
            return False
        try:
            msg = EmailMessage()
            msg["Subject"] = subject
            msg["From"] = from_mail
            msg["To"] = to
            msg.set_content(message)
            if attachments != "":
                msg = self.attach_file(msg, attachments)
            server = smtplib.SMTP(server)
            server.set_debuglevel(0)
            server.starttls()
            server.login(from_mail, password)
            server.send_message(msg)
            server.quit()
            sent = True
        except BaseException as err:
            cat = msglib.get("E6")
            msg = f"{cat} {str(err)}"
            sent = False
        finally:
            if sent == False:
                print("Fail to send email")
        return sent    

    def send_result(self, to, subject, message, attachments=""):
        sent = False
        body = ""
        try:
            # Mail connection info            
            path = fslib.get_path_config("mail.cfg")
            info = fslib.open_json(path)
            server = info["smtp"]
            from_mail = info["from"]
            password = info["password"]         
            # Basic message
            msg = MIMEMultipart('alternative')
            msg["Subject"] = subject
            msg["From"] = from_mail
            msg["To"] = to
            # General message
            part1 = MIMEText(f"{message}", 'plain')            
            msg.attach(part1)
            # HTML table with result statistics
            body = self.csv_to_str(attachments[0][const.REPORT_PATH])
            part2 = MIMEText(body, 'html')
            msg.attach(part2)
            # Attach attachments
            for i in range(0, 2):
                part = MIMEBase('application', "octet-stream")
                part.set_payload(open(attachments[i][const.REPORT_PATH], "rb").read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment', filename=attachments[i][const.REPORT_FILENAME])
                msg.attach(part)
            # Connection and send
            server = smtplib.SMTP(server)
            server.set_debuglevel(0)
            server.starttls()
            server.login(from_mail, password)
            server.send_message(msg)
            server.quit()
            sent = True
        except BaseException as err:
            cat = msglib.get("E6")
            msg = f"{cat} {str(err)}"
            sent = False
        finally:
            if sent == False:
                print("Fail to send email")
        return sent
    
    def csv_to_str(self, path):
        html_table = ""
        with open(path, "r", encoding='UTF-8') as my_input_file:
            csv_data = csv.reader(my_input_file)
            headers = next(csv_data)
            html_table = '<table>\n<tr>'
            for header in headers:
                header = header.split(";")
                for item in header:
                    html_table += f'<th>{item}</th>'
            html_table += '</tr>\n'
            for row in csv_data:
                html_table += '<tr>'
                for cell in row:
                    line = cell.split(";")
                    for item in line:
                        html_table += f'<td>{item}</td>'
                html_table += '</tr>'
            html_table += '</table>'
        return html_table
    
    def attach_file(self, msg, attachments):
        for i in range(0, 2):
            with open(attachments[i][const.REPORT_PATH], "rb") as content_file:
                content = content_file.read()
                msg.add_attachment(content, maintype="application", subtype="csv", filename=attachments[i][const.REPORT_FILENAME])
        return msg                    

    def notify_success(self, recon, reports):
        to = setuplib.tag_value(recon, "Email")        
        if to.strip() != "":
            name = setuplib.tag_value(recon, "Name")
            subject = msglib.get("M21", [name])
            body = msglib.get("M23")
            self.send_result(to, subject, body, reports)

    def notify_fail(self, recon, message):
        to = setuplib.tag_value(recon, "Email")
        if to.strip() != "":
            name = setuplib.tag_value(recon, "Name")
            subject = msglib.get("M22", [name])
            body = message
            self.send_mail(to, subject, body)      