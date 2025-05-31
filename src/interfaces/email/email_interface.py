from abc import ABC, abstractmethod

class IEmailService:

    @abstractmethod
    def send(self, to: str, subject:str, template: str, fields: dict):
        pass