from rich.console import Console
from wallet.message import Message

def print_message(msg:Message,stderr:bool=False):
    console = Console(stderr=stderr)
    console.print(msg.text,style=msg.color)


