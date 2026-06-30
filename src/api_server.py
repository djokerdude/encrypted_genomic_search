from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from Crypto.Random import get_random_bytes

from genome_database import retrieve_genome, store_genome, retrieve_all_genomes, initialize_database
from aes_storage import encrypt_sequence, decrypt_sequence
from genome_search import search_plaintext_genome
from rsa_manager import generate_keys, encrypt_key, decrypt_key

app = FastAPI(title="Encrypted Genomic Search Engine")

private_key, public_key = generate_keys()
initialize_database()

class GenomeUpload(BaseModel):
    sequence_id: str
    sequence: str

class GenomeSearch(BaseModel):
    query: str

@app.get("/")
def root():
    return {"message": "Encrypted Genomic Search Engine API"}

@app.get("/genome/{sequence_id}")
def get_genome(sequence_id: str):
    result = retrieve_genome(sequence_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"Genome '{sequence_id}' not found")
    return {"sequence_id": sequence_id, "encrypted_sequence": result[0]}

@app.post("/upload")
def upload_genome(genome: GenomeUpload):
    aes_key = get_random_bytes(32)
    encrypted_sequence = encrypt_sequence(genome.sequence, aes_key)
    encrypted_aes_key = encrypt_key(aes_key, public_key)
    store_genome(genome.sequence_id, encrypted_sequence, encrypted_aes_key)
    return {"message": "Genome uploaded successfully", "sequence_id": genome.sequence_id}

@app.post("/search")
def search_genomes(search: GenomeSearch):
    query = search.query
    all_matches = []

    for sequence_id, encrypted_sequence, encrypted_aes_key in retrieve_all_genomes():
        aes_key = decrypt_key(encrypted_aes_key, private_key)
        plaintext = decrypt_sequence(encrypted_sequence, aes_key)
        positions = search_plaintext_genome(plaintext, query)
        if positions:
            all_matches.append({"sequence_id": sequence_id, "positions": positions})

    return {"query": query, "matches": all_matches}
