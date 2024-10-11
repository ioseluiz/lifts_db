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

def get_lift_actual_start(lift_id) -> str:
    db = sqlite3.connect('lifts_4d.db')

    query = """SELECT lift.id, lift.name, pour.actual_start FROM lift
               LEFT JOIN pour ON lift.id = pour.lift_id
               WHERE lift_id = ?;"""
    
    cur = db.cursor()
    lift = cur.execute(query, (lift_id,))
    lift_data = lift.fetchone()
    if lift_data != None:
        actual_start = lift_data[2]
    else:
        actual_start =  None
    return actual_start

def get_pours_with_lift():
    db = sqlite3.connect('lifts_4d.db')

    query = """SELECT lift.id, lift.name, pour.actual_start, pour.actual_quantity FROM lift
               LEFT JOIN pour ON lift.id = pour.lift_id;
               """
    cur = db.cursor()
    lifts = cur.execute(query)
    lifts = lifts.fetchall()
    return lifts