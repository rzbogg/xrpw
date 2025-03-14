import click

from wallet.config import get_default_config
from wallet.message import Message, Msgs
from wallet.output import print_message

from wallet.manager import WalletManager
from wallet.exception import WalletException


from wallet.wallet import XWallet


@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = WalletManager(get_default_config())


@cli.command()
@click.argument('wallet-name')
@click.argument('password')
@click.pass_obj
def wallet_generate(manager: WalletManager,wallet_name:str,password:str):
    wallet = XWallet.create()
    try:
        manager.save_wallet(wallet,wallet_name,password)
        print_message(Message(Msgs.SuccesfulWalletGeneration,'green'))
    except WalletException as e:
        e.print()
 

@cli.command()
@click.argument('wallet-name')
@click.option('-p','--password',type=str,required=True, help='password for your wallet')
@click.pass_obj
def wallet_show(manager: WalletManager,wallet_name:str,password:str):
    try:
        wallet = manager.load_wallet(wallet_name,password)
        print(wallet)
    except WalletException as e:
        e.print()


# TODO: handle importing secret numbers,private keys, and mnemonic phrases

@cli.command()
@click.argument('wallet-name')
@click.option('-p','--password',type=str,required=True, help='password for your wallet')
@click.option('-s','--seed',type=str,required=True, help='family seed of the wallet')
@click.pass_obj
def wallet_import(manager: WalletManager,wallet_name:str,seed:str,password:str):
    try:
        wallet = manager.import_wallet(wallet_name,seed,password)
        click.echo(wallet)
    except WalletException as e:
        e.print()

