import binascii
import json

from wallet.message import Message, Msgs
from wallet.store import DataBase
from wallet.wallet import XWallet
from wallet.encryption import (
    encrypt,
    decrypt
)

from wallet.exception import WalletException


class WalletManager:
    def __init__(self,db:DataBase) -> None:
        self._db: DataBase = db

    def save_wallet(self,wallet:XWallet,name:str,password:str):
        if self._db.exist(f'{name}_*'):
            raise WalletException(
                Message(Msgs.DuplicateWalletName,'red')
            )
        if self._db.exist(f'*_{wallet.address_hash[0:6]}'):
            raise WalletException(
                Message(Msgs.DuplicateWalletAddress,'red')
            )

        data = wallet.to_dict()
        data['private_key'] = encrypt(data['private_key'],password).hex()
    
        file_name = f'{name}_{wallet.address_hash[0:6]}'
        if not self._db.create(file_name,json.dumps(data)):
            raise WalletException(
                Message(Msgs.WalletExist,'red')
            )
            

    def load_wallet(self,name:str,password:str) -> XWallet:
        content = self._db.read(f'{name}_*')
        if not content:
            raise WalletException(
                Message(Msgs.WalletNotFound,'red')
            )

        wallet_json = json.loads(content)
        pv = decrypt(binascii.unhexlify(wallet_json['private_key']),password)
        if not pv : 
            raise WalletException(
                Message(Msgs.InvalidPassword,'red')
            )
        
        wallet_json['private_key'] = pv
        return XWallet.from_dict(wallet_json) 

    def import_wallet(self,name:str,family_seed:str,password:str):
        try:
            wallet = XWallet.from_seed(family_seed)
        except:
            raise WalletException(
                Message(Msgs.InvalidSeed,'red')
            )
        self.save_wallet(wallet,name,password)
        return wallet

