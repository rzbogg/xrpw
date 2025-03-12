from pathlib import Path
import click

from wallet.store import DataBase

from wallet.manager import (
    WalletManager,
    WalletManagerError,
)

from wallet.wallet import XWallet


@click.group()
@click.pass_context
def cli(ctx):
    p = Path('~/.wallet_xrp')
    ctx.obj = WalletManager(DataBase(p.expanduser().resolve()))


@cli.command()
@click.argument('wallet-name')
@click.argument('password')
@click.pass_obj
def wallet_generate(manager: WalletManager,wallet_name:str,password:str):
    wallet = XWallet.create()
    try:
        manager.save_wallet(wallet,wallet_name,password)
    except WalletManagerError as e:
        click.echo(e)
 

@cli.command()
@click.argument('wallet-name')
@click.option('-p','--password',type=str,required=True, help='password for your wallet')
@click.pass_obj
def wallet_show(manager: WalletManager,wallet_name:str,password:str):
    try:
        wallet = manager.load_wallet(wallet_name,password)
        print(wallet)
    except WalletManagerError as e:
        click.echo(e)


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
    except WalletManagerError as e:
        click.echo(e)
