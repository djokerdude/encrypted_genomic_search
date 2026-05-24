from fasta_loader import load_fasta
from aes_storage import encrypt_sequence, decrypt_sequence
from genome_database import (
    initialize_database,
    store_genome,
    retrieve_genome
)

from Crypto.Random import get_random_bytes

def main():
    #initialize database
    initialize_database()

    #load genome sequences
    sequences = load_fasta("../data/sample.fasta")

    #Generate AES key
    aes_key = get_random_bytes(16)

    #Select genome
    sequence_id = "sequence_1"
    sequence = sequences[sequence_id]

    print("\nOriginal Sequence:")
    print(sequence)

    #Encrypt genome sequence
    encrypted_sequence = encrypt_sequence(sequence, aes_key)

    print("\nEncrypted Sequence:")
    print(encrypted_sequence)

    #Store encrypted genome
    store_genome(
        sequence_id,
        encrypted_sequence
    )

    print("\nGenome stored in database")

    #Retrieve encrypted genome
    retrieved_ciphertext = retrieve_genome(sequence_id)

    print("\nRetrieved Encrypted Genome:")
    print(retrieved_ciphertext)

    #Decrypt genome
    decrypted_sequence = decrypt_sequence(
        retrieved_ciphertext,
        aes_key
    )

    #Print decrypted sequence
    print("\nDecrypted Sequence:")
    print(decrypted_sequence)

if __name__ == "__main__":
    main()