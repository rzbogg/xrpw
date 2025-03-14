import click

from wallet.config import Config, get_default_config,get_default_config_testnet
from wallet.message import Message, Msgs
from wallet.output import print_message
from wallet.manager import WalletManager
from wallet.exception import WalletException

from wallet.wallet import XWallet


@click.group()
@click.pass_context
def cli(ctx):
    config = get_default_config_testnet()
    ctx.obj = WalletManager(config)


@cli.command()
@click.argument('wallet-name')
@click.argument('password')
@click.pass_obj
def wallet_generate(manager: WalletManager,wallet_name:str,password:str):
    try:
        manager.generate_wallet(wallet_name,password)
        if manager.config.dev:
            print_message(Message(Msgs.SuccesfulTestnetWalletGeneration,'green'))
            return
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


@cli.command()
@click.argument('wallet-name')
@click.option('-p','--password',type=str,required=True, help='password for your wallet')
@click.pass_obj
def account_info(manager: WalletManager, wallet_name:str, password:str):
    try:
        m = manager.account_into(wallet_name,password)
        print_message(m)
    except WalletException as e:
        e.print()



@cli.command()
@click.argument('wallet-name')
@click.option('-p','--password',type=str,required=True, help='password for your wallet')
@click.option('-r','--recipient',type=str,required=True, help='recipient for the transaction')
@click.option('-a','--amount',type=str,required=True, help='xrp amount to send')
@click.pass_obj
def send_tx(
    manager: WalletManager, 
    wallet_name:str, 
    password:str, 
    recipient:str,
    amount:str
):
    try:
        p = manager.send_tx(wallet_name,password,recipient,amount)
        print_message(p)
    except WalletException as e:
        e.print()

