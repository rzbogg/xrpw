from abc import abstractmethod
import base64
from typing_extensions import override
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from wallet.exception import WalletException
from wallet.message import Message, Msgs


class EncryptionBase:
    def __init__(self) -> None:
        pass
    
    @abstractmethod
    def encrypt(self,content:str,password:str) -> bytes:
        pass

    @abstractmethod
    def decrypt(self,content:str,password:str) -> bytes:
        pass

    @classmethod
    def name(cls) -> str:
        return cls.__name__

class EncryptionFernet(EncryptionBase):
    def __init__(self) -> None:
        super().__init__()
        self._salt:str = '123456789'


    @override
    def encrypt(self, content: str, password: str) -> bytes:
        suit = Fernet(self._to_fernet_key(password))
        enc = suit.encrypt(content.encode())
        return enc
        
    @override
    def decrypt(self,content: str | bytes,password:str)-> bytes:
        suit = Fernet(self._to_fernet_key(password))
        try:
            result = suit.decrypt(content)
            return result 
        except InvalidToken as e:
            raise WalletException(Message(Msgs.InvalidPassword,'red'))

    def _to_fernet_key(self,password:str):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self._salt.encode(),
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def get_encryption_method(name:str):
    methods = {
        EncryptionFernet.name() : EncryptionFernet(),
    }
    try:
        return methods[name]
    except KeyError:
        raise WalletException(Message(Msgs.InvalidEncryptionMethod,'red'))
