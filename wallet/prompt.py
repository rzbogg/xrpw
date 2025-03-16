from rich import prompt

def get_wallet_password(prmpt:str) -> str:
    return prompt.Prompt.ask(
        prmpt,
        password=True
    )

def get_str(prmpt:str) -> str:
    return prompt.Prompt.ask(
        prmpt,
    )

def get_int(prmpt:str) -> int:
    return prompt.IntPrompt.ask(
        prmpt
    )

def confirm(prmpt:str) -> bool:
    return prompt.Confirm.ask(
        prmpt
    )
