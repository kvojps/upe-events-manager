from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from core.infrastructure.settings.ses import SESConfig
from core.domain.subscriber import Subscriber
from core.infrastructure.settings.env_handler import settings
from core.infrastructure.shared.cloud.email_handler import EmailHandlerProvider


class EmailHandlerSESAdapter(EmailHandlerProvider):
    def __init__(self):
        self._session = SESConfig()
        self._sender = settings.EMAIL_SENDER

    def send_raw_email(self, file: bytes, listener: Subscriber) -> None:
        msg = MIMEMultipart()
        msg["Subject"] = "CERTIFICADO DE PARTICIPAÇÃO SECAP"
        msg["From"] = self._sender
        msg["To"] = listener.email

        body = f"""
        Olá {listener.name},
        
        Parabéns por participar do evento da SECAP, esperamos que tenha sido uma experiência enriquecedora.
        
        Atenciosamente,
        Equipe SECAP
        """

        msg.attach(MIMEText(body))

        attachment = MIMEBase("application", "octet-stream")
        attachment.set_payload(file)
        encoders.encode_base64(attachment)
        attachment.add_header(
            "Content-Disposition",
            f"attachment; filename=certificado-secap-{listener.name}.pdf",
        )

        msg.attach(attachment)

        try:
            self._session.ses_client().send_raw_email(
                Source=self._sender,
                Destinations=[listener.email],
                RawMessage={"Data": msg.as_string()},
            )
        except Exception as e:
            raise e
