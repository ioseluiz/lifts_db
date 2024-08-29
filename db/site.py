import sqlite3

def drop_table() -> None:
    db = sqlite3.connect('lifts_4d.db')
    DROP_TABLE = "DROP TABLE IF EXISTS site;"
    cur = db.cursor()
    cur.execute(DROP_TABLE)
    db.close()

def create_table() -> None:
    db = sqlite3.connect('lifts_4d.db')
    CREATE_SITES = """
                CREATE TABLE IF NOT EXISTS site (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                abr TEXT);
                """
    cur = db.cursor()
    cur.execute(CREATE_SITES)
    db.close()


def insert_site(name: str, abr: str) -> None:
    db = sqlite3.connect('lifts_4d.db')
    INSERT_QUERY  = """
                    INSERT INTO site(name, abr) VALUES
                    (?, ?);"""
    cur = db.cursor()
    cur.execute(INSERT_QUERY, (name, abr))
    db.commit()
    db.close()

def get_all_sites() -> list[tuple]:
    db = sqlite3.connect('lifts_4d.db')
    query = 'SELECT * FROM site;'
    cur = db.cursor()
    sites = cur.execute(query)
    sites = sites.fetchall()
    return sites

def get_site_id_by_abr(abr) -> int:
    db = sqlite3.connect('lifts_4d.db')
    query = "SELECT id FROM site WHERE abr=?;"
    cur = db.cursor()
    site = cur.execute(query, (abr,))
    site_id = site.fetchone()
    if site_id != None:
        site_id = site_id[0]
    else:
        site_id =  None
    return site_id

def update_site() -> None:
    pass

def delete_site() -> None:
    pass
