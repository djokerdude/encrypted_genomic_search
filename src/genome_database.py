import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "genomes.db"

def initialize_database():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS genomes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sequence_id TEXT UNIQUE NOT NULL,
                encrypted_sequence TEXT NOT NULL,
                encrypted_key TEXT NOT NULL
            )
        """)

def store_genome(sequence_id: str, encrypted_sequence: str, encrypted_key: str):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO genomes (sequence_id, encrypted_sequence, encrypted_key)
            VALUES (?, ?, ?)
            ON CONFLICT(sequence_id) DO UPDATE SET
                encrypted_sequence = excluded.encrypted_sequence,
                encrypted_key = excluded.encrypted_key
        """, (sequence_id, encrypted_sequence, encrypted_key))

def retrieve_genome(sequence_id: str):
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute("""
            SELECT encrypted_sequence, encrypted_key
            FROM genomes WHERE sequence_id = ?
        """, (sequence_id,)).fetchone()
    return row  # (encrypted_sequence, encrypted_key) or None

def retrieve_all_genomes():
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute("""
            SELECT sequence_id, encrypted_sequence, encrypted_key FROM genomes
        """).fetchall()
