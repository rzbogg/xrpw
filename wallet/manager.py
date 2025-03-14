import binascii
import json

from wallet.config import Config
from wallet.message import Message, Msgs
from wallet.store import DataBase
from wallet.wallet import XWallet

from wallet.exception import WalletException


class WalletManager:
    def __init__(self,config:Config) -> None:
        self.config: Config = config
        self._db: DataBase = config.database

    def save_wallet(self,wallet:XWallet,name:str,password:str):
        if self._db.exist(f'{name}_*'):
            raise WalletException(
                Message(Msgs.DuplicateWalletName,'red')
            )
        if self._db.exist(f'*_{wallet.address_hash[0:6]}'):
            raise WalletException(
                Message(Msgs.DuplicateWalletAddress,'red')
            )

        content = wallet.encrypt(password,self.config.encryption_method)
    
        file_name = f'{name}_{wallet.address_hash[0:6]}'
        if not self._db.create(file_name,content):
            raise WalletException(
                Message(Msgs.WalletExist,'red')
            )
            

    def load_wallet(self,name:str,password:str) -> XWallet:
        content = self._db.read(f'{name}_*')
        if not content:
            raise WalletException(
                Message(Msgs.WalletNotFound,'red')
            )
        return XWallet.decrypt(content,password) 
        

    def import_wallet(self,name:str,family_seed:str,password:str):
        try:
            wallet = XWallet.from_seed(family_seed)
        except:
            raise WalletException(
                Message(Msgs.InvalidSeed,'red')
            )
        self.save_wallet(wallet,name,password)
        return wallet

