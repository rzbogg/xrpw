from dataclasses import dataclass

from xrpl.clients import Client

from wallet.encryption import EncryptionBase, EncryptionFernet
from wallet.store import DataBase
from wallet.xrplapi import get_default_jsonrpc_client


@dataclass(frozen=True)
class Config:
    database: DataBase
    encryption_method: EncryptionBase
    xrpl_api: Client


def get_default_config() -> Config :
    return Config(
        database= DataBase('/home/rezbo/.wallet_xrp/'),
        encryption_method=EncryptionFernet(),
        xrpl_api= get_default_jsonrpc_client(),
    )
