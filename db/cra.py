import sqlite3

def drop_table() -> None:
    db = sqlite3.connect('lifts_4d.db')
    DROP_TABLE = "DROP TABLE IF EXISTS cra;"
    cur = db.cursor()
    cur.execute(DROP_TABLE)
    db.close()

def create_table() -> None:
    db = sqlite3.connect('lifts_4d.db')
    CREATE_CRA = """
    CREATE TABLE IF NOT EXISTS cra (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    site_id INTEGER,
    lift_id INTEGER,
    equipment_id INTEGER,
    start_date TEXT,
    FOREIGN KEY (site_id) REFERENCES site (id),
    FOREIGN KEY (lift_id) REFERENCES lift (id),
    FOREIGN KEY (equipment_id) REFERENCES equipment (id)
    );
    """
    cur = db.cursor()
    cur.execute(CREATE_CRA)
    db.close()



