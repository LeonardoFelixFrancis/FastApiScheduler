from src.interfaces.email.email_interface import IEmailService

class HostingerEmailService(IEmailService):

    def send(self, to, template, fields):
        print('Hostinger mail send.')