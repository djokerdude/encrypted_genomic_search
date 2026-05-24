from fasta_loader import load_fasta
from aes_storage import encrypt_sequence, decrypt_sequence
from rsa_manager import (
    generate_keys,
    encrypt_key,
    decrypt_key
)

from Crypto.Random import get_random_bytes

def main():
    sequences = load_fasta("../data/sample.fasta")

    sequence= sequences["sequence_1"]

    print("\nOriginal Sequence: ")
    print(sequence)

    #Generate AES key
    aes_key = get_random_bytes(16)


    #Encrypt genome sequence
    encrypted_sequence = encrypt_sequence(sequence, aes_key)

    print("\nEncrypted Sequence:")
    print(encrypted_sequence)

    #Generate RSA keys
    private_key, public_key = generate_keys()

    #Encrypt AES key with RSA public key
    encrypted_aes_key = encrypt_key(aes_key,public_key)

    print("\nEncrypted AES Key:")
    print(encrypted_aes_key)

    #Decrypt AES key with RSA private key
    decrypted_aes_key = decrypt_key(
        encrypted_aes_key,
        private_key
    )

    #Decrypt genome sequence
    decrypted_sequence = decrypt_sequence(
        encrypted_sequence,
        decrypted_aes_key
    )

    #Print decrypted sequence
    print("\nDecrypted Sequence:")
    print(decrypted_sequence)

if __name__ == "__main__":
    main()