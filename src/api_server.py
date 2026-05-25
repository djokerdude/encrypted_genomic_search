from fastapi import FastAPI
from pydantic import BaseModel
from genome_database import (
    retrieve_genome,
    store_genome
)
from aes_storage import (
    encrypt_sequence
)
from Crypto.Random import get_random_bytes

AES_KEY = get_random_bytes(16)

app = FastAPI()

#this creates the request model
class GenomeUpload(BaseModel):
    sequence_id: str
    sequence: str

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