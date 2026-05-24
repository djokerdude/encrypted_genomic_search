from collections import defaultdict

def build_kmer_index(sequences, k=3):
    index = defaultdict(list)

    for seq_id, sequence in sequences.items():

        for i in range(len(sequence) - k + 1):
            kmer = sequence[i:i+k]

            index[kmer].append( {
                "sequence_id": seq_id,
                "position": i
            })
    return dict(index)

#def generate_kmers(sequence, k=3):
    #kmers = []

    #for i in range(len(sequence) - k + 1):
        #kmer = sequence[i:i+k]
        #kmers.append((kmer,i))

   # return kmers