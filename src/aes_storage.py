from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

NONCE_SIZE = 16
TAG_SIZE = 16

def encrypt_sequence(sequence: str, key: bytes) -> str:
    nonce = get_random_bytes(NONCE_SIZE)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(sequence.encode())
    return base64.b64encode(nonce + tag + ciphertext).decode()

def decrypt_sequence(ciphertext_b64: str, key: bytes) -> str:
    data = base64.b64decode(ciphertext_b64)
    nonce = data[:NONCE_SIZE]
    tag = data[NONCE_SIZE:NONCE_SIZE + TAG_SIZE]
    ciphertext = data[NONCE_SIZE + TAG_SIZE:]
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag).decode()
