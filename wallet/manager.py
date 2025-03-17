from xrpl.core.addresscodec import classic_address_to_xaddress
from xrpl.models.transactions import Transaction 
from xrpl.transaction import submit

from wallet.config import Config
from wallet.message import Message, Msgs
from wallet.qrcode import create_and_open_qrcode
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

    def create_payment(self,name:str,password:str,recipient:str,amount:str,tag: int | None = None):
        wallet = self.load_wallet(name,password)
        return build_payment_tx(wallet,recipient,amount,self.config.xrpl_api,tag=tag)

    def send_payment(self,tx:Transaction):
        r = submit(tx,self.config.xrpl_api)
        if not r.result.get('accepted'):
            raise WalletException(
                Message(Msgs.TransactionFailed,'red')
            )
        return Message(f"Transaction completed: {r.result['tx_json']['hash']}",'green')
    
    def create_and_send_payment(self,name:str,password:str,recipient:str,amount:str):
        payment = self.create_payment(name,password,recipient,amount)
        return self.send_payment(payment)

    def wallet_exist(self,name:str) -> bool:
        return self._db.exist(name)

    def authenticate(self,name:str,password:str):
        _ = self.load_wallet(name,password)

    def info_recieve(self,name:str, password:str,tag: int | None = None, qr: bool = False):
        wallet = self.load_wallet(name,password)
        result = f'Classic address: {wallet.address}'
        if tag:
            x_address = classic_address_to_xaddress(wallet.address,tag,is_test_network = True if self.config.dev else False)
            result += f'\nX-Address: {x_address}'
        if qr:
            create_and_open_qrcode(wallet.address)
        return result
