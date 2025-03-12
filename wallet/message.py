from enum import Enum
from typing import NamedTuple

class Msgs(Enum):

    def __str__(self) -> str:
        return self.value

    InvalidPassword = 'password is wrong.'
    DuplicateWalletName = 'a wallet with the same name exists, try another one.'
    DuplicateWalletAddress = 'a wallet with the same address exists, try another one.'
    WalletExist = 'the wallet already exists.'
    WalletNotFound = 'wallet not found'
    InvalidSeed = 'the provided seed is invalid'

class Message(NamedTuple):
    text: Msgs
    color: str





