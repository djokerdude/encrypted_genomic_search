from fasta_loader import load_fasta
from dna_encoder import encode_dna
from kmer_indexer import generate_kmers

def main():
    sequences = load_fasta("../data/sample.fasta")

    for seq_id, sequence in sequences.items():
        print(f"\n=== {seq_id} ===")

        encoded = encode_dna(sequence)
        print(f"Encoded : {encoded}")

        kmers = generate_kmers(sequence, k=3)

        print("\n3-mers:")
        for kmer, position in kmers:
            print(f"{kmer} at position {position}")

if __name__ == "__main__":
    main()