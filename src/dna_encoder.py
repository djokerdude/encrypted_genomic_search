DNA_ENCODING = {
    "A": "00",
    "C": "01",
    "G": "10",
    "T": "11"
}

def encode_dna(sequence):
    binary = ""

    for nucleotide in sequence:
        binary += DNA_ENCODING[nucleotide]

    return binary