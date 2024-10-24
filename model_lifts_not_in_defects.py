import sqlite3
from db import structure
from db import site
from db import pour, lift, defect
from datetime import datetime

def get_lifts_not_in_model(site_id: int, structure_id: int):
    # Get all lifts
    lifts = lift.get_lifts_filter_by_structure(site_id, structure_id)

    # Get all lifts related to defects
    defects = defect.get_all_defects_with_lift(site_id, structure_id)
    data_lifts = []
    for item in lifts:
        data_lifts.append(item[0])

    data_defects = []
    for item in defects:
        data_defects.append(item[0])

    # print(f"Defects: {len(defects)}, Lifts: {len(lifts)}")


    # Get model lifts that are not in defects
    not_included = []
    for item in data_lifts:
        if item not in data_defects:
            not_included.append(item)

    data_for_check = []

    for x in not_included:
        lift_data = lift.get_lift_with_actual_start(x)
        lift_actual_start_str = lift_data[1]
        lift_name = lift_data[0]
        lift_actual_start_datetime = datetime.strptime(lift_actual_start_str, '%m/%d/%Y')
        if lift_actual_start_datetime <= datetime(2013, 12, 31, 23, 59):
            # print(lift_name)
            data_for_check.append({"lift": lift_name, "actual_start": lift_actual_start_datetime})

        

    # print(f"Lifts in model but not in defects spreadsheet: {len(not_included)}")

    return data_for_check


def get_info_site(site_id: int) -> list[dict]:
     # Upper East
    upper_east = get_lifts_not_in_model(site_id, 10)
    # Upper West
    upper_west = get_lifts_not_in_model(site_id, 11)
    # Middle East
    middle_east = get_lifts_not_in_model(site_id, 12)
    # Middle West
    middle_west = get_lifts_not_in_model(site_id, 13)
    # Lower east
    lower_east = get_lifts_not_in_model(site_id, 14)
    # Lower West
    lower_west = get_lifts_not_in_model(site_id,15)
    # LH1
    lh1_east = get_lifts_not_in_model(site_id,16)
    lh1_center = get_lifts_not_in_model(site_id,17)
    lh1_west = get_lifts_not_in_model(site_id,18)
    # LH2
    lh2_east = get_lifts_not_in_model(site_id,19)
    lh2_center = get_lifts_not_in_model(site_id,20)
    lh2_west = get_lifts_not_in_model(site_id,21)
    # LH3
    lh3_east = get_lifts_not_in_model(site_id,22)
    lh3_center = get_lifts_not_in_model(site_id,23)
    lh3_west = get_lifts_not_in_model(site_id,24)
    # LH4
    lh4_east = get_lifts_not_in_model(site_id,25)
    lh4_center = get_lifts_not_in_model(site_id,26)
    lh4_west = get_lifts_not_in_model(site_id,27)

    # Conduits
    cc1 = get_lifts_not_in_model(site_id,6)
    cc2 = get_lifts_not_in_model(site_id,5)
    cc3 = get_lifts_not_in_model(site_id,4)
    cc4 = get_lifts_not_in_model(site_id,3)
    cc5 = get_lifts_not_in_model(site_id, 1)
    cc6 = get_lifts_not_in_model(site_id, 2)

    # Crossunders
    cu1 = get_lifts_not_in_model(site_id,7)
    cu2 = get_lifts_not_in_model(site_id,8)
    cu3 = get_lifts_not_in_model(site_id,9)

    # Trifurcations
    tf1 = get_lifts_not_in_model(site_id,32)
    tf2 = get_lifts_not_in_model(site_id,33)
    tf3 = get_lifts_not_in_model(site_id,34)
    tf4 = get_lifts_not_in_model(site_id,35)
    tf5 = get_lifts_not_in_model(site_id,36)
    tf6 = get_lifts_not_in_model(site_id,37)

    # Valve Structures
    vs1 = get_lifts_not_in_model(site_id, 44)
    vs2 = get_lifts_not_in_model(site_id, 45)
    vs3 = get_lifts_not_in_model(site_id, 46)
    vs4 = get_lifts_not_in_model(site_id, 47)
    vs5 = get_lifts_not_in_model(site_id, 48)
    vs6 = get_lifts_not_in_model(site_id, 49)

    # T Conduits
    t1 = get_lifts_not_in_model(site_id,38)
    t2 = get_lifts_not_in_model(site_id,39)
    t3 = get_lifts_not_in_model(site_id,40)
    t4 = get_lifts_not_in_model(site_id,41)
    t5 = get_lifts_not_in_model(site_id,42)
    t6 = get_lifts_not_in_model(site_id,43)





    lifts = upper_east + upper_west + middle_east + middle_west + lower_east + lower_west
    lifts += lh1_east + lh1_center + lh1_west
    lifts += lh2_east + lh2_center + lh2_west
    lifts += lh3_east + lh3_center + lh3_west
    lifts += lh4_east + lh4_center + lh4_west
    lifts += cc1 + cc2 + cc3 + cc3 + cc4 + cc5 + cc6
    lifts += cu1 + cu2 + cu3
    lifts += tf1 + tf2 + tf3 + tf4 + tf5 + tf6
    lifts += vs1 + vs2 + vs3 + vs4 + vs5 + vs6
    lifts += t1 + t2 + t3 + t4 + t5 + t6


    return lifts

def main():
    # PACIFIC
    pac_lifts_not_model = []
    pac_lifts_not_model = get_info_site(1)

    for x in pac_lifts_not_model:
        print(x)

    print(f"Cantidad {len(pac_lifts_not_model)}")

    # ATLANTIC
    atl_lifts_not_model = []
    atl_lifts_not_model = get_info_site(2)

    for x in atl_lifts_not_model:
        print(x)
    
    print(f"Cantidad {len(atl_lifts_not_model)}")
   

    
    

if __name__ == "__main__":
    main()