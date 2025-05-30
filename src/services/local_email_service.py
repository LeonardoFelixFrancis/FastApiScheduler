from src.interfaces.email.email_interface import IEmailService

class LocalEmailService(IEmailService):

    def send(self, to, template, fields):
        pass