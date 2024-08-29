import sqlite3

def drop_table() -> None:
    db = sqlite3.connect('lifts_4d.db')
    DROP_TABLE = "DROP TABLE IF EXISTS name_fix_defect;"
    cur = db.cursor()
    cur.execute(DROP_TABLE)
    db.close()

def create_table() -> None:
    db = sqlite3.connect('lifts_4d.db')
    CREATE_LIFTS = """
    CREATE TABLE IF NOT EXISTS name_fix_defect (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lift TEXT,
    defects INTEGER,
    ncr INTEGER,
    cod INTEGER,
    fix_code INTEGER,
    description TEXT,
    solution TEXT,
    name_fix TEXT,
    defects_fix INTEGER,
    ncr_fix INTEGER,
    cod_fix INTEGER
    );
    """
    cur = db.cursor()
    cur.execute(CREATE_LIFTS)
    db.close()

def insert_name_fix_defect(lift: str, defects: int, ncr: int, cod: int, fix_code: int, 
                           description: str, solution: str, name_fix: str, defects_fix: int, ncr_fix: int, cod_fix: int) -> None:
    db = sqlite3.connect('lifts_4d.db')
    INSERT_QUERY  = """
                    INSERT INTO name_fix_defect (lift, defects, ncr, cod, fix_code, description, solution,name_fix,
                      defects_fix, ncr_fix, cod_fix) VALUES
                    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?);"""
    cur = db.cursor()
    cur.execute(INSERT_QUERY, (lift, defects, ncr, cod, fix_code, description, solution,name_fix, defects_fix,
                               ncr_fix, cod_fix))
    db.commit()
    db.close()

def get_all_name_fix_defects() -> list[tuple]:
    db = sqlite3.connect('lifts_4d.db')
    query = 'SELECT * FROM name_fix_defect;'
    cur = db.cursor()
    fixes = cur.execute(query)
    fixes = fixes.fetchall()
    return fixes

def get_fix_by_lift(lift: str) -> int:
    db = sqlite3.connect('lifts_4d.db')
    query = "SELECT * FROM name_fix_defect WHERE lift=?;"
    cur = db.cursor()
    lift = cur.execute(query, (lift,))
    lift_data = lift.fetchone()
    if lift_data != None:
        lift_data = lift_data
    else:
        lift_data =  None
    return lift_data



