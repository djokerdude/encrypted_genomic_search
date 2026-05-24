def generate_kmers(sequence, k=3):
    kmers = []

    for i in range(len(sequence) - k + 1):
        kmer = sequence[i:i+k]
        kmers.append((kmer,i))
        
    return kmers