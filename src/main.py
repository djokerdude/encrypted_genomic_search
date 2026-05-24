from fasta_loader import load_fasta
from kmer_indexer import build_kmer_index
from genome_search import search_kmer


def main():
    sequences = load_fasta("../data/sample.fasta")

    print("\nBuilding k-mer index...")
    index = build_kmer_index(sequences, k=3)

    print("\nSearching for 'ACT'...\n")

    results = search_kmer(index, "ACT")

    if results:
        for result in results:
            print(
                f"Found in {result['sequence_id']} "
                f"at position {result['position']}"
            )
    else:
        print("No matches found")

if __name__ == "__main__":
    main()