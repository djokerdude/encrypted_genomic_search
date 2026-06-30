from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from pathlib import Path
import base64

KEY_PATH = Path(__file__).parent.parent / "keys" / "private_key.pem"

def load_or_generate_keys(passphrase: str = ""):
    """Load the RSA key pair from disk, generating and saving it if absent."""
    KEY_PATH.parent.mkdir(exist_ok=True)
    if KEY_PATH.exists():
        private_key = RSA.import_key(
            KEY_PATH.read_bytes(),
            passphrase=passphrase or None
        )
    else:
        private_key = RSA.generate(2048)
        pem = private_key.export_key(
            format="PEM",
            passphrase=passphrase or None,
            protection="scryptAndAES256-CBC" if passphrase else None,
        )
        KEY_PATH.write_bytes(pem)
    return private_key, private_key.publickey()

def generate_keys():
    key = RSA.generate(2048)
    return key, key.publickey()

def encrypt_key(aes_key: bytes, public_key) -> str:
    cipher = PKCS1_OAEP.new(public_key)
    return base64.b64encode(cipher.encrypt(aes_key)).decode()

def decrypt_key(encrypted_key_b64: str, private_key) -> bytes:
    cipher = PKCS1_OAEP.new(private_key)
    return cipher.decrypt(base64.b64decode(encrypted_key_b64))
