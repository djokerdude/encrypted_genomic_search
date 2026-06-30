# Encrypted Genomic Search Engine

A FastAPI service for storing and searching genomic sequences with AES-256-GCM encryption and RSA hybrid key management. Each sequence is encrypted with a unique AES key; that key is RSA-OAEP-wrapped so the server never holds a reusable plaintext secret.

## Architecture

```
Upload:   sequence  ──► AES-256-GCM ──► ciphertext
          AES key   ──► RSA-2048-OAEP ► encrypted_key
          SQLite: { sequence_id, ciphertext, encrypted_key }

Search:   per-row: encrypted_key ──► RSA decrypt ──► AES key
                   ciphertext    ──► AES-GCM decrypt ──► plaintext ──► match
```

**Why AES-GCM?** Authenticated encryption — the tag detects any ciphertext tampering before decryption. No padding-oracle risk. The nonce, tag, and ciphertext are packed into the stored blob.

**Why per-sequence keys?** Compromise of one row's AES key does not affect any other sequence.

**RSA key lifetime:** The key pair is generated fresh on each server start (ephemeral). In production this would be replaced by a KMS-backed key.

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run the API

```bash
cd src
uvicorn api_server:app --reload
```

Interactive docs: http://localhost:8000/docs

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/upload` | Encrypt and store a genomic sequence |
| GET | `/genome/{sequence_id}` | Return the stored ciphertext for a sequence |
| POST | `/search` | Search a query substring across all stored sequences |

### Upload a sequence

```bash
curl -X POST http://localhost:8000/upload \
  -H "Content-Type: application/json" \
  -d '{"sequence_id": "seq1", "sequence": "ATCGATCGATCGTTAG"}'
```

### Search across all sequences

```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "ATCG"}'
```

Response:
```json
{
  "query": "ATCG",
  "matches": [
    {"sequence_id": "seq1", "positions": [0, 4, 8]}
  ]
}
```

### Retrieve stored ciphertext

```bash
curl http://localhost:8000/genome/seq1
```

## Run the CLI demo

```bash
cd src
python main.py
```

Demonstrates: FASTA loading, 2-bit DNA encoding, AES-256-GCM encryption, RSA key wrapping, SQLite round-trip, and k-mer index search.

## Module overview

| File | Purpose |
|------|---------|
| `aes_storage.py` | AES-256-GCM encrypt/decrypt with packed nonce+tag+ciphertext |
| `rsa_manager.py` | RSA-2048 key generation and PKCS1-OAEP key wrapping |
| `genome_database.py` | SQLite persistence with upsert semantics |
| `genome_search.py` | Linear scan search; k-mer index-assisted search |
| `kmer_indexer.py` | O(1) k-mer lookup index over plaintext sequences |
| `fasta_loader.py` | BioPython FASTA parser |
| `dna_encoder.py` | 2-bit binary encoding (A=00, C=01, G=10, T=11) |
| `api_server.py` | FastAPI service wiring all modules together |
| `main.py` | CLI walkthrough of the full pipeline |

## Key management

The RSA private key is stored at `keys/private_key.pem` (gitignored). On first start the server generates and saves it; on subsequent starts it loads the existing key, so sequences remain decryptable across restarts.

Set `KEY_PASSPHRASE` to encrypt the key file at rest with scrypt + AES-256:

```bash
export KEY_PASSPHRASE="your-passphrase"
uvicorn api_server:app --reload
```

Without `KEY_PASSPHRASE` the key is saved as an unencrypted PEM — acceptable for local development, not for production. In production, replace `load_or_generate_keys` with a KMS-backed equivalent and remove `keys/` entirely.
