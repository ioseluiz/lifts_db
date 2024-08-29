import sqlite3

def drop_table() -> None:
    db = sqlite3.connect('lifts_4d.db')
    DROP_TABLE = "DROP TABLE IF EXISTS cdslift;"
    cur = db.cursor()
    cur.execute(DROP_TABLE)
    db.close()

def create_table() -> None:
    db = sqlite3.connect('lifts_4d.db')
    CREATE_DEFECTS = """
    CREATE TABLE IF NOT EXISTS cdslift (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cds_id INTEGER,
    lift_id INTEGER,
    FOREIGN KEY (cds_id) REFERENCES cds (id),
    FOREIGN KEY (lift_id) REFERENCES lift (id)
    );
    """
    cur = db.cursor()
    cur.execute(CREATE_DEFECTS)
    db.close()
    
def insert_cdslift(cds_id: int, lift_id: int) -> None:
    db = sqlite3.connect('lifts_4d.db')
    INSERT_QUERY  = """
                    INSERT INTO cdslift (cds_id, lift_id) VALUES
                    (?, ?);"""
    cur = db.cursor()
    cur.execute(INSERT_QUERY, (cds_id, lift_id))
    db.commit()
    db.close()