
from xrpl.clients.sync_client import SyncClient
from xrpl.account import get_balance, does_account_exist

from wallet.message import Message, Msgs


class Account:
    def __init__(self,address:str, client: SyncClient) -> None:
        self.address:str = address
        self.client:SyncClient = client

    @property
    def exist(self) -> bool:
        return does_account_exist(self.address,self.client)

    @property
    def balance(self):
        'in xrp' 
        return get_balance(self.address,self.client)

    def account_info(self):
        if not self.exist:
            return Message(
                Msgs.InactiveAccount,
                'red'
            )
        result = f'Address: {self.address}\nBalance: {self.balance}'
        return Message(
            result,
            'white'
        )
