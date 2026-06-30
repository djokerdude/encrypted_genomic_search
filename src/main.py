from fasta_loader import load_fasta
from aes_storage import encrypt_sequence, decrypt_sequence
from genome_database import initialize_database, store_genome, retrieve_genome
from kmer_indexer import build_kmer_index
from genome_search import search_sequence
from dna_encoder import encode_dna
from rsa_manager import generate_keys, encrypt_key, decrypt_key
from Crypto.Random import get_random_bytes

def main():
    initialize_database()
    sequences = load_fasta("../data/sample.fasta")

    print("=== Hybrid Encryption Demo ===")
    private_key, public_key = generate_keys()
    print("Generated RSA-2048 key pair")

    sequence_id = "sequence_1"
    sequence = sequences[sequence_id]
    print(f"\nOriginal sequence ({len(sequence)} bp):")
    print(sequence[:80], "..." if len(sequence) > 80 else "")

    # Binary encoding
    print("\n=== 2-bit DNA Encoding ===")
    binary = encode_dna(sequence[:12])
    print(f"First 12 bp: {sequence[:12]}  →  {binary}")

    # Per-sequence AES-256 key, RSA-encrypted for storage
    aes_key = get_random_bytes(32)
    encrypted_key = encrypt_key(aes_key, public_key)
    encrypted_sequence = encrypt_sequence(sequence, aes_key)
    print("\n=== Encryption ===")
    print(f"AES-256-GCM ciphertext (first 60 chars): {encrypted_sequence[:60]}...")
    print(f"RSA-encrypted AES key (first 60 chars):  {encrypted_key[:60]}...")

    store_genome(sequence_id, encrypted_sequence, encrypted_key)
    print("\nStored in database.")

    # Retrieve and decrypt
    result = retrieve_genome(sequence_id)
    recovered_key = decrypt_key(result[1], private_key)
    decrypted = decrypt_sequence(result[0], recovered_key)
    print(f"\nDecrypted matches original: {decrypted == sequence}")

    # K-mer index search
    print("\n=== K-mer Index Search (k=3) ===")
    index = build_kmer_index(sequences, k=3)
    query = sequence[:6]
    print(f"Query: {query}")
    matches = search_sequence(index, sequences, query, k=3)
    for m in matches[:3]:
        print(f"  Found in {m['sequence_id']} at position {m['position']}")

if __name__ == "__main__":
    main()
