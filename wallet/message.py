from enum import Enum
from typing import NamedTuple

class Msgs(Enum):

    def __str__(self) -> str:
        return self.value

    # errors
    InvalidPassword = 'password is wrong.'
    DuplicateWalletName = 'a wallet with the same name exists, try another one.'
    DuplicateWalletAddress = 'a wallet with the same address exists, try another one.'
    WalletExist = 'the wallet already exists.'
    WalletNotFound = 'wallet not found'
    InvalidSeed = 'the provided seed is invalid'
    InvalidEncryptionMethod = 'the encryption method in the json content in invalid'
    # 
    SuccesfulWalletGeneration = 'a wallet has been succesfully generated.'

class Message(NamedTuple):
    text: str|Msgs
    color: str





