from rich.console import Console

from wallet.message import Message

def print_error(msg:Message):
    console = _get_console(stderr=True)
    console.print(msg.text,style=msg.color)

def _get_console(stderr=False):
    return Console(stderr=stderr)

