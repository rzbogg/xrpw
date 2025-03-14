from xrpl.clients.sync_client import SyncClient
from xrpl.models.transactions import Payment
from xrpl.core.addresscodec import is_valid_classic_address 
from xrpl.transaction import autofill_and_sign,autofill, submit

from wallet.config import Config
from wallet.message import Message, Msgs
from wallet.store import DataBase
from wallet.transaction import build_payment_tx
from wallet.wallet import XWallet
from wallet.account import Account
from wallet.exception import WalletException


class WalletManager:
    def __init__(self,config:Config) -> None:
        self.config: Config = config
        self._db: DataBase = config.database

    def save_wallet(self,wallet:XWallet,name:str,password:str):
        if self._db.exist(name):
            raise WalletException(
                Message(Msgs.DuplicateWalletName,'red')
            )
        if self._db.exist(name):
            raise WalletException(
                Message(Msgs.DuplicateWalletAddress,'red')
            )

        content = wallet.encrypt(password,self.config.encryption_method)
    
        if not self._db.create(name,content):
            raise WalletException(
                Message(Msgs.WalletExist,'red')
            )

    def generate_wallet(self,name:str,password:str):
        wallet = None 
        if self.config.dev: 
            wallet = XWallet.create_testnet(self.config.xrpl_api)
        else:
            wallet = XWallet.create()

        file_name = f'{name}_{wallet.address_hash[0:6]}'
        self.save_wallet(wallet,file_name,password)
            

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


    def account_into(self,name:str,password:str) -> Message:
        wallet = self.load_wallet(name,password)
        account = Account(wallet.address,self.config.xrpl_api)
        return account.account_info()

    def send_tx(self,name:str,password:str,recipient:str,amount:str):
        wallet = self.load_wallet(name,password)
        # signed tx
        tx = build_payment_tx(wallet,recipient,amount,self.config.xrpl_api)
        r = submit(tx,self.config.xrpl_api)
        if not r.result.get('accepted'):
            raise WalletException(
                Message(Msgs.TransactionFailed,'red')
            )
        return Message(f"Transaction completed: #{r.result['tx_json']['hash']}",'green')
