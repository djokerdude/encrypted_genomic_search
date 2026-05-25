from fastapi import FastAPI
from pydantic import BaseModel
from genome_database import (
    retrieve_genome,
    store_genome,
    retrieve_all_genomes,
    initialize_database
)
from aes_storage import (
    encrypt_sequence,
    decrypt_sequence
)

from genome_search import (
    search_plaintext_genome
)
from Crypto.Random import get_random_bytes

AES_KEY = b"1234567890abcdef"

app = FastAPI()
initialize_database()

#this creates the request model
class GenomeUpload(BaseModel):
    sequence_id: str
    sequence: str

class GenomeSearch(BaseModel):
    query: str

@app.get("/")
def root():

    return {
        "message": "Encrypted Genomic Search Engine API"
    }

@app.get("/genome/{sequence_id}")
def get_genome(sequence_id: str):
    encrypted_genome = retrieve_genome(sequence_id)

    if encrypted_genome:

        return {
            "sequence_id": sequence_id,
            "encrypted_genome": encrypted_genome
        }
    return {
        "error": "Genome not found"
    }

@app.post("/upload")
def upload_genome(genome: GenomeUpload):

    encrypted_sequence = encrypt_sequence(
        genome.sequence,
        AES_KEY
    )

    store_genome(
        genome.sequence_id,
        encrypted_sequence
    )

    return {
        "message": "Genome uploaded successfully",
        "sequence_id": genome.sequence_id
    }

@app.post("/search")
def search_genomes(search: GenomeSearch):

    query = search.query
    genomes = retrieve_all_genomes()

    all_matches = []

    for sequence_id, encrypted_sequence in genomes:
        
        decrypted_sequence = decrypt_sequence(
            encrypted_sequence,
            AES_KEY
        )

        positions = search_plaintext_genome(
            decrypted_sequence,
            query
        )

        if positions:

            all_matches.append({
                "sequence_id": sequence_id,
                "positions": positions
            })
    return {
        "query": query,
        "matches": all_matches
    }