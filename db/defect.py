import sqlite3
from db import lift

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
    formwork_defects INTEGER,
    rebar_defects INTEGER,
    FOREIGN KEY (lift_id) REFERENCES lift (id)
    );
    """
    cur = db.cursor()
    cur.execute(CREATE_DEFECTS)
    db.close()

def insert_defect(lift_id: int, icl_found: str, qty_defects: int, ncr: int, cod: int, formwork: int, rebar: int) -> None:
    db = sqlite3.connect('lifts_4d.db')
    INSERT_QUERY  = """
                    INSERT INTO defect (lift_id, icl_found, defects, ncr, cod, formwork_defects, rebar_defects) VALUES
                    (?, ?, ?, ?, ?, ?, ?);"""
    cur = db.cursor()
    cur.execute(INSERT_QUERY, (lift_id, icl_found, qty_defects, ncr, cod, formwork, rebar))
    db.commit()
    db.close()

def get_all_defects() -> list[tuple]:
    db = sqlite3.connect('lifts_4d.db')
    query = 'SELECT * FROM defect;'
    cur = db.cursor()
    defects = cur.execute(query)
    defects = defects.fetchall()
    return defects

def get_all_defects_with_lift(site_id: int, structure_id: int) -> list[tuple]:
    db = sqlite3.connect('lifts_4d.db')
    query = """
                SELECT lift.name, defect.lift_id, defect.icl_found, defect.defects FROM defect
                LEFT JOIN lift ON lift.id = defect.lift_id
                WHERE lift.site_id = ? AND lift.structure_id = ?;
            """
    cur = db.cursor()
    lifts = cur.execute(query, (site_id, structure_id))
    lifts = lifts.fetchall()
    return lifts