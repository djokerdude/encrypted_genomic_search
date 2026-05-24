def search_kmer(index,query):
    return index.get(query, [])

def search_sequence(index, sequences, query, k=3):
    matches = []

    first_kmer = query[:k]

    candidate_locations = index.get(first_kmer, [])

    for candidate in candidate_locations:
        seq_id = candidate["sequence_id"]
        start_pos = candidate["position"]

        full_sequence = sequences[seq_id]

        extracted = full_sequence[start_pos:start_pos + len(query)]

        if extracted == query:
            matches.append({
                "sequence_id": seq_id,
                "position": start_pos,
                "match": extracted
            })
            
    return matches