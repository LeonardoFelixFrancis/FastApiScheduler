from abc import ABC, abstractmethod

class IEmailService:

    @abstractmethod
    def send(self, to: str, template: str, fields: dict):
        pass