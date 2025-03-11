import hashlib

from xrpl.wallet import Wallet
from xrpl.constants import CryptoAlgorithm


class XWallet(Wallet):
    def __init__(self, public_key: str, private_key: str, *, master_address: str | None = None, seed: str | None = None, algorithm: CryptoAlgorithm | None = None) -> None:
        super().__init__(public_key, private_key, master_address=master_address, seed=seed, algorithm=algorithm)
        self._address_hash: str | None  = None

    @property
    def address_hash(self):
        if not self._address_hash:
            self._address_hash = hashlib.sha1(self.address.encode('utf-8')).digest().hex()
        return self._address_hash


    def to_dict(self) -> dict[str,str]:
        return {
            'address': self.address,
            'public_key': self.public_key,
            'private_key': self.private_key,
        }

    @classmethod
    def from_dict(cls,d:dict[str,str]):
        return cls(
            public_key = d['public_key'],
            private_key = d['private_key'],
            master_address = d['address'],
        )
    
