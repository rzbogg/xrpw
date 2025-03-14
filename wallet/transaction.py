from xrpl.clients.sync_client import SyncClient
from xrpl.core.addresscodec.codec import is_valid_classic_address
from xrpl.models.transactions import Payment 
from xrpl.transaction import autofill_and_sign 

from wallet.exception import WalletException
from wallet.message import Message, Msgs
from wallet.wallet import XWallet


def build_payment_tx(sender: XWallet, recipient: str, amount:str,client:SyncClient):
    if not is_valid_classic_address(recipient):
        raise WalletException(
            Message(Msgs.InvalidRecipientAddress, 'red')
        )
    payment = Payment(account=sender.classic_address,amount=amount,destination=recipient)
    return autofill_and_sign(
        payment,
        client,
        sender,
    )
