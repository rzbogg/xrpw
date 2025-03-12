import binascii
import json
from ossaudiodev import control_labels

from wallet.store import DataBase
from wallet.wallet import XWallet
from wallet.encryption import (
    encrypt,
    decrypt
)


class WalletManagerError(Exception):
    pass

class DuplicateNameError(WalletManagerError):
    pass

class DuplicateAddressError(WalletManagerError):
    pass

class DuplicateWalletError(WalletManagerError):
    pass

class WalletNotFoundError(WalletManagerError):
    pass

class WrongPasswordError(WalletManagerError):
    pass

class InvalidSeedError(WalletManagerError):
    pass


class WalletManager:
    def __init__(self,db:DataBase) -> None:
        self._db: DataBase = db

    def save_wallet(self,wallet:XWallet,name:str,password:str):
        if self._db.exist(f'{name}_*'):
            raise DuplicateNameError
        if self._db.exist(f'*_{wallet.address_hash[0:6]}'):
            raise DuplicateAddressError

        data = wallet.to_dict()
        data['private_key'] = encrypt(data['private_key'],password).hex()
    
        file_name = f'{name}_{wallet.address_hash[0:6]}'
        if not self._db.create(file_name,json.dumps(data)):
            raise DuplicateWalletError
            

    def load_wallet(self,name:str,password:str) -> XWallet:
        content = self._db.read(f'{name}_*')
        if not content:
            raise WalletNotFoundError

        wallet_json = json.loads(content)
        pv = decrypt(binascii.unhexlify(wallet_json['private_key']),password)
        if not pv : 
            raise WrongPasswordError
        
        wallet_json['private_key'] = pv
        return XWallet.from_dict(wallet_json) 

    def import_wallet(self,name:str,family_seed:str,password:str):
        try:
            wallet = XWallet.from_seed(family_seed)
        except:
            raise InvalidSeedError
        self.save_wallet(wallet,name,password)
        return wallet

