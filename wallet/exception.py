from wallet.message import Message
from wallet.output import print_message
from rich import get_console

class WalletException(Exception):
    def __init__(self, msg:Message,*args: object) -> None:
        super().__init__(*args)
        self.msg = msg

    def print(self):
        print_message(self.msg)
