import fastapi
import smtplib

from pydantic import BaseModel
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from src.core.config import settings


class EmailRequest(BaseModel):
    body: str
    email: str


def send_email(body, email, attachment=None, filename=None):
    sender_email = settings.SENDER_EMAIL
    sender_password = settings.SENDER_PASSWORD
    recipient_email = settings.RECIPIENT_EMAIL

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email

    msg.attach(MIMEText(body, 'plain'))

    if attachment and filename:
        part = MIMEApplication(attachment, Name=filename)
        part['Content-Disposition'] = f'attachment; filename="{filename}"'
        msg.attach(part)

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
    except Exception as exc:
        raise fastapi.HTTPException(
            status_code=500,
            detail=str(exc)
        )
