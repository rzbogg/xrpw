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
    SuccesfulTestnetWalletGeneration = 'a testnet wallet has been succesfully generated.'
    # account
    InactiveAccount = 'Account is not activated on xrp ledger. please deposit 1 xrp to activate it'
    # transaction
    InvalidRecipientAddress = 'recepient address is invalid'
    TransactionFailed = 'Transaction failed!'

class Message(NamedTuple):
    text: str|Msgs
    color: str





