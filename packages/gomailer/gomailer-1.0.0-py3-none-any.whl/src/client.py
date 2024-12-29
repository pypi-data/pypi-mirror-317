from .automation import Automation
from .contacts import Contacts
from .mailing import Mailing


class Client:
    def __init__(self, api_key):
        self.api_key = api_key

    def automation(self):
        return Automation(self.api_key)

    def contacts(self):
        return Contacts(self.api_key)

    def mailing(self):
        return Mailing(self.api_key)
