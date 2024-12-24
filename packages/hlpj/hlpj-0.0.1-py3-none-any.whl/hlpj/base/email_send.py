import smtplib
import ssl
from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from email_validator import validate_email

from . import helpers


class Email:
    def __init__(
        self, host: str, port: int, from_: str, password: str, subject: str, to: str
    ):
        validate_email(from_)
        self.host = host
        self.port = port
        self.from_ = from_
        self.to = to
        self.password = password

        for address in to.split(","):
            validate_email(address)

        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = from_
        message["To"] = to
        self.message = message

    def text_body(self, body: str):
        text_part = MIMEText(body, "plain")
        self.message.attach(text_part)
        return self

    def attach(self, file_str: str):
        file_path = Path(file_str)
        content = file_path.read_bytes()
        part = MIMEBase("application", "octet-stream")
        part.set_payload(content)
        encoders.encode_base64(part)
        file_name = helpers.sanitize_filename(file_path.name).replace(" ", "_")
        part.add_header("Content-Disposition", f"attachment; filename={file_name}")
        self.message.attach(part)
        return self

    def send(self):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.host, self.port, context=context) as server:
            server.login(self.from_, self.password)
            try:
                server.sendmail(
                    self.from_, self.to.split(","), self.message.as_string()
                )
                timestamp = str(datetime.now())
                return "Enviado em " + timestamp
            except Exception as e:
                return e.__class__.__name__
