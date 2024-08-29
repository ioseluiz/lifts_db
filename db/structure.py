import sqlite3

def drop_table() -> None:
    db = sqlite3.connect('lifts_4d.db')
    DROP_TABLE = "DROP TABLE IF EXISTS structure;"
    cur = db.cursor()
    cur.execute(DROP_TABLE)
    db.close()

def create_table() -> None:
    db = sqlite3.connect('lifts_4d.db')
    CREATE_STRUCTURES = """
                    CREATE TABLE IF NOT EXISTS structure (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    abr TEXT);
                    """
    cur = db.cursor()
    cur.execute(CREATE_STRUCTURES)
    db.close()

def insert_structure(name: str, abr: str) -> None:
    db = sqlite3.connect('lifts_4d.db')
    INSERT_QUERY  = """
                    INSERT INTO structure(name, abr) VALUES
                    (?, ?);"""
    cur = db.cursor()
    cur.execute(INSERT_QUERY, (name, abr))
    db.commit()
    db.close()

def get_all_structures() -> list[tuple]:
    db = sqlite3.connect('lifts_4d.db')
    query = 'SELECT * FROM structure;'
    cur = db.cursor()
    structures = cur.execute(query)
    structures = structures.fetchall()
    return structures

def get_structure_id_by_abr(abr) -> int:
    db = sqlite3.connect('lifts_4d.db')
    query = "SELECT id FROM structure WHERE abr=?;"
    cur = db.cursor()
    structure = cur.execute(query, (abr,))
    structure_id = structure.fetchone()
    if structure_id != None:
        structure_id = structure_id[0]
    else:
        structure_id =  None
    return structure_id