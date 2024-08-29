import sqlite3

def drop_table() -> None:
    db = sqlite3.connect('lifts_4d.db')
    DROP_TABLE = "DROP TABLE IF EXISTS equipment;"
    cur = db.cursor()
    cur.execute(DROP_TABLE)
    db.close()

def create_table() -> None:
    db = sqlite3.connect('lifts_4d.db')
    CREATE_EQUIPMENT = """
                CREATE TABLE IF NOT EXISTS equipment (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                equipment_type TEXT);
                """
    cur = db.cursor()
    cur.execute(CREATE_EQUIPMENT)
    db.close()

def insert_equipment(name: str, type: str) -> None:
    db = sqlite3.connect('lifts_4d.db')
    INSERT_QUERY  = """
                    INSERT INTO equipment (name, equipment_type) VALUES
                    (?, ?);"""
    cur = db.cursor()
    cur.execute(INSERT_QUERY, (name, type))
    db.commit()
    db.close()

def get_all_equipment() -> list[tuple]:
    db = sqlite3.connect('lifts_4d.db')
    query = 'SELECT * FROM equipment;'
    cur = db.cursor()
    equipment = cur.execute(query)
    equipment = equipment.fetchall()
    return equipment

def get_equipment_id_by_name(name) -> int:
    db = sqlite3.connect('lifts_4d.db')
    query = "SELECT id FROM equipment WHERE name=?;"
    cur = db.cursor()
    equipment = cur.execute(query, (name,))
    equipment_id = equipment.fetchone()
    if equipment != None:
        equipment_id = equipment_id[0]
    else:
        equipment_id =  None
    return equipment_id





