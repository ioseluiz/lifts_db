import sqlite3

def drop_table() -> None:
    db = sqlite3.connect('lifts_4d.db')
    DROP_TABLE = "DROP TABLE IF EXISTS cds;"
    cur = db.cursor()
    cur.execute(DROP_TABLE)
    db.close()

def create_table() -> None:
    db = sqlite3.connect('lifts_4d.db')
    CREATE_CDS = """
    CREATE TABLE IF NOT EXISTS cds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_name TEXT,
    qty_equipment int,
    volume_report NUMERIC,
    concrete_start TEXT,
    concrete_finish TEXT,
    duration NUMERIC,
    calc_duration NUMERIC,
    rate NUMERIC,
    calc_rate NUMERIC,
    source TEXT
    );
    """
    cur = db.cursor()
    cur.execute(CREATE_CDS)
    db.close()
    
def insert_cds(report_name: str, qty_equipment: int, volume: float, start: str, finish: str, duration:float,
               calc_duration: float, rate: float, calc_rate: float, source: str) -> None:
    db = sqlite3.connect('lifts_4d.db')
    INSERT_QUERY  = """
                    INSERT INTO cds (report_name, qty_equipment, volume_report, concrete_start, concrete_finish,
                    duration, calc_duration, rate, calc_rate, source) VALUES
                    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
    cur = db.cursor()
    cur.execute(INSERT_QUERY, (report_name, qty_equipment, volume, start, finish, duration, calc_duration,
                               rate, calc_rate, source))
    db.commit()
    db.close()
    
def get_report_id_by_name(report) -> int:
    db = sqlite3.connect('lifts_4d.db')
    query = "SELECT id FROM cds WHERE report_name=?;"
    cur = db.cursor()
    cds = cur.execute(query, (report,))
    cds_id = cds.fetchone()
    if cds_id != None:
        cds_id = cds_id[0]
    else:
        cds_id =  None
    return cds_id