from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

def pad(data):
    while len(data) % 16 != 0:
        data += " "

    return data

def encrypt_sequence(sequence, key):
    cipher = AES.new(key,AES.MODE_ECB)
    padded = pad(sequence)
    encrypted_bytes = cipher.encrypt(padded.encode())

    return base64.b64encode(encrypted_bytes).decode()

def decrypt_sequence(ciphertext, key):
    cipher = AES.new(key, AES.MODE_ECB)

    decoded = base64.b64decode(ciphertext)

    decrypted = cipher.decrypt(decoded)

    return decrypted.decode().rstrip()
