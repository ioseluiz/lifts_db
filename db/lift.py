import sqlite3

def drop_table() -> None:
    db = sqlite3.connect('lifts_4d.db')
    DROP_TABLE = "DROP TABLE IF EXISTS lift;"
    cur = db.cursor()
    cur.execute(DROP_TABLE)
    db.close()

def create_table() -> None:
    db = sqlite3.connect('lifts_4d.db')
    CREATE_LIFTS = """
    CREATE TABLE IF NOT EXISTS lift (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    site_id INTEGER,
    structure_id INTEGER,
    monolith TEXT,
    lift TEXT,
    name TEXT,
    design_quantity NUMERIC,
    FOREIGN KEY (site_id) REFERENCES site (id),
    FOREIGN KEY (structure_id) REFERENCES structure (id)
    );
    """
    cur = db.cursor()
    cur.execute(CREATE_LIFTS)
    db.close()

def insert_lift(site: int, structure: id, monolith: str, lift: str, name: str, design_quantity: float) -> None:
    db = sqlite3.connect('lifts_4d.db')
    INSERT_QUERY  = """
                    INSERT INTO lift (site_id, structure_id, monolith, lift, name, design_quantity) VALUES
                    (?, ?, ?, ?, ?, ?);"""
    cur = db.cursor()
    cur.execute(INSERT_QUERY, (site, structure, monolith, lift, name, design_quantity))
    db.commit()
    db.close()

def get_all_lifts() -> list[tuple]:
    db = sqlite3.connect('lifts_4d.db')
    query = 'SELECT * FROM lift;'
    cur = db.cursor()
    lifts = cur.execute(query)
    lifts = lifts.fetchall()
    return lifts

def get_lift_id_by_name(name) -> int:
    db = sqlite3.connect('lifts_4d.db')
    query = "SELECT id FROM lift WHERE name=?;"
    cur = db.cursor()
    lift = cur.execute(query, (name,))
    lift_id = lift.fetchone()
    if lift_id != None:
        lift_id = lift_id[0]
    else:
        lift_id =  None
    return lift_id

def get_lift_name_by_name(name) -> str:
    db = sqlite3.connect('lifts_4d.db')
    query = "SELECT id FROM lift WHERE name=?;"
    cur = db.cursor()
    lift = cur.execute(query, (name,))
    lift_id = lift.fetchone()
    if lift_id != None:
        lift_id = lift_id[0]
    else:
        lift_id =  "lift don't exists."
    return lift_id

# get all lifts is name is contained in lift_name
def get_lifts_that_contain_name(lift_name) -> str:
    db = sqlite3.connect('lifts_4d.db')
    query = "SELECT id, name FROM lift WHERE instr(lower(name), lower(?));"
    # query = "SELECT id, name FROM lift WHERE name LIKE '%?%';"
    cur = db.cursor()
    lifts = cur.execute(query, (lift_name,))
    lifts = lifts.fetchall()
    print(lifts)
    if len(lifts) == 0:
        print(lift_name)
        print(lifts)
    return lifts

def get_lifts_with_pours():
    db = sqlite3.connect('lifts_4d.db')

def get_lifts_filter_by_structure(site_id: int, structure_id: int) -> list[tuple]:
    db = sqlite3.connect('lifts_4d.db')
    query = """
                SELECT lift.name, structure.abr, structure.name FROM lift
                LEFT JOIN structure ON structure.id = lift.structure_id
                WHERE lift.site_id = ? AND lift.structure_id = ?;
            """
    cur = db.cursor()
    lifts = cur.execute(query, (site_id, structure_id))
    lifts = lifts.fetchall()
    return lifts


def get_lift_with_actual_start(liftname: str):
    db = sqlite3.connect('lifts_4d.db')
    query = """
            SELECT lift.name, pour.actual_start FROM lift
            LEFT JOIN pour ON lift.id = pour.lift_id
            WHERE lift.name = ?
            """
    cur = db.cursor()
    lift = cur.execute(query, (liftname,))
    lift_id = lift.fetchone()
    if lift_id != None:
        lift_id = lift_id
    else:
        lift_id =  "lift don't exists."
    return lift_id

