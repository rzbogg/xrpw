from dataclasses import dataclass

from xrpl.clients.sync_client import SyncClient

from wallet.encryption import EncryptionBase, EncryptionFernet
from wallet.store import DataBase
from wallet.xrplapi import get_default_jsonrpc_client, get_default_jsonrpc_client_testnet


@dataclass(frozen=True)
class Config:
    database: DataBase
    encryption_method: EncryptionBase
    xrpl_api: SyncClient
    dev: bool = False


def get_default_config() -> Config :
    return Config(
        database= DataBase('/home/rezbo/.wallet_xrp/'),
        encryption_method=EncryptionFernet(),
        xrpl_api= get_default_jsonrpc_client(),
    )

def get_default_config_testnet() -> Config :
    return Config(
        database= DataBase('/home/rezbo/.wallet_xrp/'),
        encryption_method=EncryptionFernet(),
        xrpl_api= get_default_jsonrpc_client_testnet(),
        dev = True
    )
