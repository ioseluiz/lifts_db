import sqlite3

def drop_table() -> None:
    db = sqlite3.connect('lifts_4d.db')
    DROP_TABLE = "DROP TABLE IF EXISTS ncn;"
    cur = db.cursor()
    cur.execute(DROP_TABLE)
    db.close()

def create_table() -> None:
    db = sqlite3.connect('lifts_4d.db')
    CREATE_NCNs = """
    CREATE TABLE IF NOT EXISTS ncn (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    site_id INTEGER,
    structure_id INTEGER,
    lift_id INTEGER,
    number TEXT,
    title TEXT,
    date TEXT,
    FOREIGN KEY (site_id) REFERENCES site (id),
    FOREIGN KEY (structure_id) REFERENCES structure (id),
    FOREIGN KEY (lift_id) REFERENCES lift (id)
    );
    """
    cur = db.cursor()
    cur.execute(CREATE_NCNs)
    db.close()

def insert_ncn(site: int, structure: id, lift: int, number: str, title: str, ncn_date: str) -> None:
    db = sqlite3.connect('lifts_4d.db')
    INSERT_QUERY  = """
                    INSERT INTO ncn (site_id, structure_id, lift_id, number, title, date) VALUES
                    (?, ?, ?, ?, ?, ?);"""
    cur = db.cursor()
    cur.execute(INSERT_QUERY, (site, structure, lift, number, title, ncn_date))
    db.commit()
    db.close()

def get_all_lifts() -> list[tuple]:
    db = sqlite3.connect('lifts_4d.db')
    query = 'SELECT * FROM lift;'
    cur = db.cursor()
    lifts = cur.execute(query)
    lifts = lifts.fetchall()
    return lifts


