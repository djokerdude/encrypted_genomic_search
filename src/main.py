from fasta_loader import load_fasta
from kmer_indexer import build_kmer_index
from genome_search import search_sequence


def main():
    sequences = load_fasta("../data/sample.fasta")

    print("\nBuilding k-mer index...")
    index = build_kmer_index(sequences, k=3)

    query = "ACTGACT"

    print(f"\nSearching for '{query}'...\n")

    results = search_sequence(index, sequences, query, k=3)

    if results:
        for result in results:
            print(
                f"Match found in  {result['sequence_id']} "
                f"at position {result['position']}"
            )
    else:
        print("No matches found")

if __name__ == "__main__":
    main()