import click

from wallet.config import get_default_config_testnet
from wallet.message import Message, Msgs
from wallet.manager import WalletManager
from wallet.exception import WalletException
from wallet.output import print_message
from wallet.prompt import confirm, get_wallet_password
from wallet.transaction import payment_overview



@click.group()
@click.pass_context
def cli(ctx):
    config = get_default_config_testnet()
    ctx.obj = WalletManager(config)


@cli.command()
@click.argument('wallet-name')
@click.option('-p','--password',type=str,required=True, help='password for your wallet')
@click.pass_obj
def wallet_generate(manager: WalletManager,wallet_name:str,password:str):
    try:
        manager.generate_wallet(wallet_name,password)
    except WalletException as e:
        e.print()
    else:
        if manager.config.dev:
            print_message(Message(Msgs.SuccesfulTestnetWalletGeneration,'green'))
            return
        print_message(Message(Msgs.SuccesfulWalletGeneration,'green'))

 

@cli.command()
@click.argument('wallet-name')
@click.option('-p','--password',type=str,required=True, help='password for your wallet')
@click.pass_obj
def wallet_show(manager: WalletManager,wallet_name:str,password:str):
    try:
        wallet = manager.load_wallet(wallet_name,password)
    except WalletException as e:
        e.print()
    else:
        print(wallet)



# TODO: handle importing secret numbers,private keys, and mnemonic phrases

@cli.command()
@click.argument('wallet-name')
@click.option('-p','--password',type=str,required=True, help='password for your wallet')
@click.option('-s','--seed',type=str,required=True, help='family seed of the wallet')
@click.pass_obj
def wallet_import(manager: WalletManager,wallet_name:str,seed:str,password:str):
    try:
        wallet = manager.import_wallet(wallet_name,seed,password)
    except WalletException as e:
        e.print()
    else:
        click.echo(wallet)



@cli.command()
@click.argument('wallet-name')
@click.option('-p','--password',type=str,required=False, help='password for your wallet')
@click.pass_obj
def account_info(manager: WalletManager, wallet_name:str, password:str):
    try:
        m = manager.account_into(wallet_name,password)
    except WalletException as e:
        e.print()
    else:
        print_message(m)


@cli.command()
@click.argument('wallet-name')
@click.option('-p','--password',type=str,required=True, help='password for your wallet')
@click.option('-r','--recipient',type=str,required=True, help='recipient for the transaction')
@click.option('-a','--amount',type=str,required=True, help='xrp amount to send')
@click.pass_obj
def send(
    manager: WalletManager, 
    wallet_name:str, 
    password:str, 
    recipient:str,
    amount:str
):
    try:
        payment = manager.create_payment(
            wallet_name,
            password,
            recipient,
            amount,
        )
        click.echo(
            payment_overview(payment)
        )
        if not confirm('do you want to proceed?'):
            return
        confirm_password = get_wallet_password('sign it with password')
        manager.authenticate(wallet_name,confirm_password)
        m = manager.send_payment(payment)

    except WalletException as e:
        e.print()
    else:
        print_message(m)

@cli.command()
@click.argument('wallet-name')
@click.option('-p','--password',type=str,required=True, help='password for your wallet')
@click.option('-qr',type=str,required=True, help='password for your wallet')
@click.pass_obj
def receive(manager: WalletManager,wallet_name:str, password:str):
    try:
        info = manager.receive_info(wallet_name,password)
    except WalletException as e:
        e.print()
    else:
        print(info)
