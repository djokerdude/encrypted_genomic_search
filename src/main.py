from fasta_loader import load_fasta
from aes_storage import encrypt_sequence, decrypt_sequence
from Crypto.Random import get_random_bytes


def main():
    sequences = load_fasta("../data/sample.fasta")

    key = get_random_bytes(16)

    sequence= sequences["sequence_1"]

    print("\nOriginal Sequence: ")
    print(sequence)

    encrypted = encrypt_sequence(sequence, key)
    print("\nEncrypted Sequence:")
    print(encrypted)

    decrypted = decrypt_sequence(encrypted, key)

    print("\nDecrypted Sequence:")
    print(decrypted)

if __name__ == "__main__":
    main()