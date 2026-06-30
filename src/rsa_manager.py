from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

def generate_keys():
    key = RSA.generate(2048)
    return key, key.publickey()

def encrypt_key(aes_key: bytes, public_key) -> str:
    cipher = PKCS1_OAEP.new(public_key)
    return base64.b64encode(cipher.encrypt(aes_key)).decode()

def decrypt_key(encrypted_key_b64: str, private_key) -> bytes:
    cipher = PKCS1_OAEP.new(private_key)
    return cipher.decrypt(base64.b64decode(encrypted_key_b64))
