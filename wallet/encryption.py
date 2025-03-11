import base64
import json
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from wallet.wallet import XWallet


def to_fernet_key(password:str,salt:str= '123456789'):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt.encode(),
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def decrypt(data: bytes,password:str)-> bytes | None:
    suit = Fernet(to_fernet_key(password))
    try:
        result = suit.decrypt(data)
        return result 
    except InvalidToken as e:
        return None

def encrypt(data:str,password:str) -> bytes :
    suit = Fernet(to_fernet_key(password))
    enc = suit.encrypt(data.encode())
    return enc
