import sqlite3

def drop_table() -> None:
    db = sqlite3.connect('lifts_4d.db')
    DROP_TABLE = "DROP TABLE IF EXISTS pour;"
    cur = db.cursor()
    cur.execute(DROP_TABLE)
    db.close()

def create_table() -> None:
    db = sqlite3.connect('lifts_4d.db')
    CREATE_POURS = """
    CREATE TABLE IF NOT EXISTS pour (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lift_id INTEGER,
    actual_start TEXT,
    actual_end TEXT,
    actual_quantity NUMERIC,
    number_pours INTEGER,
    FOREIGN KEY (lift_id) REFERENCES lift (id)
    );
    """
    cur = db.cursor()
    cur.execute(CREATE_POURS)
    db.close()

def insert_pour(lift_id: int, actual_start: str, actual_end: str, actual_quantity: float, number_pours: int) -> None:
    db = sqlite3.connect('lifts_4d.db')
    INSERT_QUERY  = """
                    INSERT INTO pour (lift_id, actual_start, actual_end, actual_quantity, number_pours) VALUES
                    (?, ?, ?, ?, ?);"""
    cur = db.cursor()
    cur.execute(INSERT_QUERY, (lift_id, actual_start, actual_end, actual_quantity, number_pours))
    db.commit()
    db.close()

def get_all_pours() -> list[tuple]:
    db = sqlite3.connect('lifts_4d.db')
    query = 'SELECT * FROM pour;'
    cur = db.cursor()
    pours = cur.execute(query)
    pours = pours.fetchall()
    return pours