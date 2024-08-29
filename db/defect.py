import sqlite3

def drop_table() -> None:
    db = sqlite3.connect('lifts_4d.db')
    DROP_TABLE = "DROP TABLE IF EXISTS defect;"
    cur = db.cursor()
    cur.execute(DROP_TABLE)
    db.close()

def create_table() -> None:
    db = sqlite3.connect('lifts_4d.db')
    CREATE_DEFECTS = """
    CREATE TABLE IF NOT EXISTS defect (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lift_id INTEGER,
    icl_found TEXT,
    defects INTEGER,
    ncr INTEGER,
    cod INTEGER,
    FOREIGN KEY (lift_id) REFERENCES lift (id)
    );
    """
    cur = db.cursor()
    cur.execute(CREATE_DEFECTS)
    db.close()

def insert_defect(lift_id: int, icl_found: str, qty_defects: int, ncr: int, cod: int) -> None:
    db = sqlite3.connect('lifts_4d.db')
    INSERT_QUERY  = """
                    INSERT INTO defect (lift_id, icl_found, defects, ncr, cod) VALUES
                    (?, ?, ?, ?, ?);"""
    cur = db.cursor()
    cur.execute(INSERT_QUERY, (lift_id, icl_found, qty_defects, ncr, cod))
    db.commit()
    db.close()

def get_all_defects() -> list[tuple]:
    db = sqlite3.connect('lifts_4d.db')
    query = 'SELECT * FROM defect;'
    cur = db.cursor()
    defects = cur.execute(query)
    defects = defects.fetchall()
    return defects