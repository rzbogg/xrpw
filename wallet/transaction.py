from xrpl.clients.sync_client import SyncClient
from xrpl.core.addresscodec.codec import is_valid_classic_address
from xrpl.models.transactions import Payment
from xrpl.transaction import autofill_and_sign 
from xrpl.utils import drops_to_xrp


from wallet.exception import WalletException
from wallet.message import Message, Msgs
from wallet.wallet import XWallet


def build_payment_tx(sender: XWallet, recipient: str, amount:str,client:SyncClient,tag: int | None = None):
    if not is_valid_classic_address(recipient):
        raise WalletException(
            Message(Msgs.InvalidRecipientAddress, 'red')
        )
    payment = Payment(account=sender.classic_address,amount=amount,destination=recipient,destination_tag=tag)
    return autofill_and_sign(
        payment,
        client,
        sender,
    )

def payment_overview(payment:Payment):
    sender = payment.account
    receiver = payment.destination
    tag = payment.destination_tag
    amount = payment.amount
    fee = payment.fee 
    tag = payment.destination_tag or 'NO-TAG'
    return f'''From: {sender}
To: {receiver}
Amount: {drops_to_xrp(str(amount))} XRP
Fee : {drops_to_xrp(fee) if fee is not None else ''} XRP
Destination tag: {tag}
'''
