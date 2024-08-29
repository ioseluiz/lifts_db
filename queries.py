import sqlite3
from db import structure
from db import site

def get_lifts_with_defects(site_abr, structure_abr, monolith):
    db = sqlite3.connect("lifts_4d.db")
    
    query = """SELECT pour.actual_start,site.abr, structure.abr, lift.name, lift.monolith,defect.defects, defect.ncr, defect.cod,defect.icl_found
        FROM defect
        LEFT JOIN lift ON defect.lift_id = lift.id
        LEFT JOIN site ON lift.site_id = site.id
        LEFT JOIN structure ON lift.structure_id = structure.id
        LEFT JOIN pour ON defect.lift_id = pour.lift_id
        WHERE site.abr = ? AND structure.abr = ? AND lift.monolith = ?;"""
    
    cur = db.cursor()
    lifts = cur.execute(query, (site_abr, structure_abr, monolith))
    lifts = lifts.fetchall()
    data = []
    for lift in lifts:
        data.append(lift)
    return data

def get_lifts_by_site_structure(site_abr, structure_abr, monolith):
    db = sqlite3.connect("lifts_4d.db")

    query = """SELECT lift.id, name, pour.actual_start FROM lift
               LEFT JOIN pour ON lift.id = pour.lift_id
               WHERE site_id = ? AND structure_id = ? AND monolith = ?;"""
    
    # Get structure_id
    structure_id = structure.get_structure_id_by_abr(structure_abr)
    # Get site_id
    site_id = site.get_site_id_by_abr(site_abr)
    cur = db.cursor()
    lifts = cur.execute(query, (site_id, structure_id, monolith))
    lifts = lifts.fetchall()
    data = []
    for lift in lifts:
        data.append(lift)
    return data
    


def main():
    lifts = get_lifts_with_defects("P", "LW","M06")
    for lift in lifts:
        print(lift)

    print("-----------------------------------\n")
    all_lifts = get_lifts_by_site_structure("P", "LW", "M06")
    for lift in all_lifts:
        print(lift)


if __name__ == "__main__":
    main()