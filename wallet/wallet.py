from binascii import unhexlify
import hashlib
import json
from mailbox import Message

from cryptography.fernet import InvalidToken
from xrpl.wallet import Wallet
from xrpl.constants import CryptoAlgorithm

from wallet.encryption import (
    EncryptionBase,
    EncryptionFernet,
    get_encryption_method
)
from wallet.exception import WalletException
from wallet.message import Msgs


class XWallet(Wallet):
    def __init__(self, public_key: str, private_key: str, *, master_address: str | None = None, seed: str | None = None, algorithm: CryptoAlgorithm | None = None) -> None:
        super().__init__(public_key, private_key, master_address=master_address, seed=seed, algorithm=algorithm)
        self._address_hash: str | None  = None

    @property
    def address_hash(self):
        if not self._address_hash:
            self._address_hash = hashlib.sha1(self.address.encode('utf-8')).digest().hex()
        return self._address_hash


    def encrypt(self,password:str,method: EncryptionBase) -> str:
        content = self.to_dict()
        content['private_key'] = method.encrypt(content['private_key'],password).hex()
        content['encryption_method'] = method.name()
        return json.dumps(content)


    def to_dict(self) -> dict[str,str]:
        return {
            'public_key': self.public_key,
            'private_key': self.private_key,
        }

    @classmethod
    def decrypt(cls,content:str,password:str):
        js = json.loads(content)
        method = get_encryption_method(js['encryption_method'])
        pk_bytes = unhexlify(js['private_key'])
        js['private_key'] = method.decrypt(pk_bytes,password)
        return XWallet.from_dict(js)

    @classmethod
    def from_dict(cls,d:dict[str,str]):
        return cls(
            public_key = d['public_key'],
            private_key = d['private_key'],
        )
    
