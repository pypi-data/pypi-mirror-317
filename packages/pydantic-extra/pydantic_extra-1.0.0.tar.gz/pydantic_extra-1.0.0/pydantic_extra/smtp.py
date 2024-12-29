__all__ = ['MailServer']

from smtplib import SMTP, SMTP_SSL

from pydantic import BaseModel, SecretStr, model_validator
from typing_extensions import Self


class MailServer(BaseModel):
    smtp_host: str
    smtp_port: int = 465
    smtp_ssl: bool = True
    smtp_login: str
    smtp_password: SecretStr
    from_addr: str = None

    @model_validator(mode='after')
    def checks(self) -> Self:
        if self.from_addr is None:
            self.from_addr = self.smtp_login
        return self

    def connect(self) -> SMTP:
        """Возвращает объект smtplib.SMTP с указанным адресом"""
        if self.smtp_ssl:
            cls = SMTP_SSL
        else:
            cls = SMTP
        return cls(self.smtp_host, self.smtp_port)

    def login(self, smtp: SMTP):
        """Выполняет авторизацию для SMTP подключения"""
        smtp.login(self.smtp_login, self.smtp_password.get_secret_value())
