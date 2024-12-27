import smtplib
from email.message import EmailMessage


class SmtpSSL:
    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def send_emsg(self, data):
        emsg = EmailMessage()
        emsg["Subject"] = data["subject"]
        emsg.set_content(data["content"])

        if data.get("From") is None:
            emsg["From"] = self.user

        emsg["To"] = data["to"]

        if "cc" in data:
            emsg["Cc"] = data["cc"]

        if "bcc" in data:
            emsg["Bcc"] = data["bcc"]

        # print(emsg)

        with smtplib.SMTP_SSL(self.host, self.port) as smtp:
            # smtp.set_debuglevel(1)
            smtp.login(self.user, self.password)
            senderrs = smtp.send_message(emsg)
        return senderrs
