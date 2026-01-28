import os, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def send_mail(subject: str, body: str, to_emails: list[str], attachments: list[str] = None):
    host = os.getenv("SMTP_HOST"); port = int(os.getenv("SMTP_PORT", "587"))
    user = os.getenv("SMTP_USER"); pwd = os.getenv("SMTP_PASS")
    msg = MIMEMultipart()
    msg["Subject"] = subject; msg["From"] = user; msg["To"] = ", ".join(to_emails)
    msg.attach(MIMEText(body, "plain", "utf-8"))
    for fpath in attachments or []:
        with open(fpath, "rb") as f:
            part = MIMEApplication(f.read())
            part.add_header("Content-Disposition","attachment", filename=os.path.basename(fpath))
            msg.attach(part)
    with smtplib.SMTP(host, port) as s:
        s.starttls(); s.login(user, pwd); s.send_message(msg)
