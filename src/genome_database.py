import sqlite3

def initialize_database():
    connection = sqlite3.connect("../data/genomes.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS genomes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sequence_id TEXT,
            encrypted_sequence TEXT
        )
    """)

    connection.commit()
    connection.close()

def store_genome(sequence_id, encrypted_sequence):
    connection = sqlite3.connect("../data/genomes.db")

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO genomes(
            sequence_id,
            encrypted_sequence
        )
        VALUES (?, ?)
    """, (sequence_id, encrypted_sequence))

    connection.commit()
    connection.close()

def retrieve_genome(sequence_id):
    connection = sqlite3.connect("../data/genomes.db")

    cursor = connection.cursor()

    cursor.execute("""
        SELECT encrypted_sequence
        FROM genomes
        WHERE sequence_id = ?
    """, (sequence_id,))

    result = cursor.fetchone()

    connection.close()

    if result:
        return result[0]
    
    return None

def retrieve_all_genomes():

    connection = sqlite3.connect("../data/genomes.db")

    cursor = connection.cursor()

    cursor.execute("""
        SELECT sequence_ID, encrypted_sequence
        FROM genomes
    """)

    results = cursor.fetchall()

    connection.close()

    return results