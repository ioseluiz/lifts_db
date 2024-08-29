import os
import csv
# import pandas as pd
from pathlib import Path
from db import site
from db import structure
from db import lift
from db import pour
from db import name_fix_defect
from db import defect
from db import equipment
from db import cra
from db import ncn
from db import cds
from db import cds_lift

ROOT_FOLDER = os.getcwd()
DATA_FOLDER = Path(ROOT_FOLDER) / "4DModel_csv"
DEFECTS_FOLDER = Path(ROOT_FOLDER) / "internal_defects"
CRA_FOLDER = Path(ROOT_FOLDER) / "CRA"
NCN_FOLDER = Path(ROOT_FOLDER) / "NCN"
EQUIPMENT_FOLDER = Path(ROOT_FOLDER) / "equipment"
CDS_FOLDER = Path(ROOT_FOLDER) /"CDS"

def save_csv(extracted_data:list[dict], headers: list[str], new_filename: str) -> None:
    """Save the data extracted from excel file (xlsx) in csv file

    Args:
        extracted_data (list[dict]): List of dictionaries with the data
                                     extracted from each row of the excel file.
        headers (list[str]): List of fields (column names) and keys of the dicts in extracted_data.
        new_filename (str): Name of the csv file that will be generated.
    """
    with open(new_filename, 'w',newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(extracted_data)
        print(f"File {new_filename} generated successfully...")

def read_csv(path_file: str,) -> list[dict]:
    with open(path_file, 'r') as csv_file:
        reader = csv.DictReader(csv_file)

        # Convert to dictionary
        result = [row for row in reader]
        return result

def main():
    data = []
    data_defects = []
    errors_lifts = []
    lifts_defects_for_fix = []
    lifts_cra_for_fix = []
    print("Read 4D Model Data from csv files")
    files = os.listdir(DATA_FOLDER)
    print(f"Folder 4DModel_csv contains {len(files)} files.")
    
    for file in files:
        full_file_path = str(Path(DATA_FOLDER) / file)
        info = read_csv(full_file_path)
        print("----------------------------------------------------------------------------\n")
        print(full_file_path)
        data += info

    # 4D Model Database as Dataframe
    # df = pd.DataFrame(data=data)
    # print(df.columns)
    # structures = df['Structure'].unique()
    structures_dict = [
        {'name': 'Conduit 5', 'abr': 'CC5'},
        {'name': 'Conduit 6', 'abr': 'CC6'},
        {'name': 'Conduit 4', 'abr': 'CC4'},
        {'name': 'Conduit 3', 'abr': 'CC3'},
        {'name': 'Conduit 2', 'abr': 'CC2'},
        {'name': 'Conduit 1', 'abr': 'CC1'},
        {'name': 'Crossunder 1', 'abr': 'CU1'},
        {'name': 'Crossunder 2', 'abr': 'CU2'},
        {'name': 'Crossunder 3', 'abr': 'CU3'},
        {'name': 'Upper East', 'abr': 'UE'},
        {'name': 'Upper West', 'abr': 'UW'},
        {'name': 'Middle East', 'abr': 'ME'},
        {'name': 'Middle West', 'abr': 'MW'},
        {'name': 'Lower East', 'abr': 'LE'},
        {'name': 'Lower West', 'abr': 'LW'},
        {'name': 'Lockhead 1 East', 'abr': 'H1E'},
        {'name': 'Lockhead 1 Center', 'abr': 'H1C'},
        {'name': 'Lockhead 1 West', 'abr': 'H1W'},
        {'name': 'Lockhead 2 East', 'abr': 'H2E'},
        {'name': 'Lockhead 2 Center', 'abr': 'H2C'},
        {'name': 'Lockhead 2 West', 'abr': 'H2W'},
        {'name': 'Lockhead 3 East', 'abr': 'H3E'},
        {'name': 'Lockhead 3 Center', 'abr': 'H3C'},
        {'name': 'Lockhead 3 West', 'abr': 'H3W'},
        {'name': 'Lockhead 4 East', 'abr': 'H4E'},
        {'name': 'Lockhead 4 Center', 'abr': 'H4C'},
        {'name': 'Lockhead 4 West', 'abr': 'H4W'},

    ]

    # 4D Model Database - SQLite

    ## Drop tables if exists
    site.drop_table()
    structure.drop_table()
    lift.drop_table()
    pour.drop_table()
    name_fix_defect.drop_table()
    defect.drop_table()
    equipment.drop_table()
    cra.drop_table()
    ncn.drop_table()
    cds.drop_table()
    cds_lift.drop_table()
    
    

    ## Create tables if not exists
    site.create_table()
    structure.create_table()
    lift.create_table()
    pour.create_table()
    name_fix_defect.create_table()
    defect.create_table()
    equipment.create_table()
    cra.create_table()
    ncn.create_table()
    cds.create_table()
    cds_lift.create_table()

    # Insert Data in Sites
    site.insert_site("Pacific", "P")
    site.insert_site("Atlantic", "A")

    # Get all sites
    sites = site.get_all_sites()
   
    # Insert Data in Structures
    for item in structures_dict:
        structure.insert_structure(item['name'], item['abr'])

    # Get all structures
    structures = structure.get_all_structures()
   
    # Insert lifts
    for item in data:
        try:
            # print(item)
            ## Get structure id
            structure_id = structure.get_structure_id_by_abr(item["Structure"])
            ## Get site id by abr
            site_id = site.get_site_id_by_abr(item["Side"])
            monolith = item["Monolith"]
            lift_data = item["Lift"]
            name = item["Name"]
            design_quantity = item["Design Quantity"]
            if structure_id:
                lift.insert_lift(site_id, structure_id, monolith, lift_data, name, design_quantity)
        except Exception as e:
            errors_lifts.append(f"Lift: {item['Name']} -- Error message: {e}")

    # Insert Pours Data
    
    for item in data:
        try:
            ## Get structure id
            structure_id = structure.get_structure_id_by_abr(item["Structure"])
            # Get lift id by name
            lift_id = lift.get_lift_id_by_name(item['Name'])
            actual_start = item["Actual Start"]
            actual_end = item["Actual End"]
            actual_quantity = item["Actual Quantity"]
            number_pours = item["Number of Pours"]
            if structure_id:
                pour.insert_pour(lift_id, actual_start, actual_end, actual_quantity, number_pours)
        except Exception as e:
            errors_lifts.append(f"Lift: {item['Name']} -- Error message: {e}")

        for item in errors_lifts:
            print(item)

    # Create names fixes for defects lifts table
    defects_names_fixes_file = str(Path(ROOT_FOLDER)/"fixes_lift_defects"/"lifts_defects_for_fix.csv")
    fixes_data = read_csv(defects_names_fixes_file)
    for fix in fixes_data:
        lift_fix_name = fix["lift"]
        defects_fix_name = fix["defects"]
        ncr_fix_name = fix["ncr"]
        cod_fix_name = fix["cod"]
        code_fix_name = fix["fix_code"]
        description_fix_name = fix["description"]
        solution_fix_name = fix["solution"]
        name_fixed = fix["name_fix"]
        defects_fixed = fix["defects_fix"]
        ncr_fixed = fix["ncr_fix"]
        cod_fixed = fix["cod_fix"]

        name_fix_defect.insert_name_fix_defect(lift_fix_name, defects_fix_name, ncr_fix_name,
                                               cod_fix_name, code_fix_name, description_fix_name,
                                               solution_fix_name,name_fixed, defects_fixed,
                                               ncr_fixed, cod_fixed)


    # Create defects table
    allowed_structures = ["UE","UW","ME","MW","LE","LW",
                          "H1C","H1E","H1W","H2C","H2E","H2W",
                          "H3C","H3E","H3W","H4C","H4E","H4W"]
    defects_files = os.listdir(DEFECTS_FOLDER)
    for file in defects_files:
        full_file_path = str(Path(DEFECTS_FOLDER) / file)
        defects_csv = read_csv(full_file_path)
        data_defects += defects_csv

    for row in data_defects:
        lift_name_defects = row["name"]
        lift_structure = row["structure"]
        if lift_structure in allowed_structures:
            # Check if a fix should be applied to the lift
            lift_for_fix = name_fix_defect.get_fix_by_lift(lift_name_defects)
            if lift_for_fix != None:
                # apply fix to lift
                # print(lift_for_fix)
                correct_lift_name = lift_for_fix[8]
                correct_defects = lift_for_fix[9]
                correct_ncr = lift_for_fix[10]
                correct_cod = lift_for_fix[11]
                if "," in correct_lift_name:
                    lifts_for_correction = correct_lift_name.split(",")
                    lifts_for_correction = [x.replace(" ","") for x in lifts_for_correction]
                    print(lifts_for_correction)
                    for fix_lift_name in lifts_for_correction:
                        lift_db = lift.get_lift_name_by_name(fix_lift_name)
                        if lift_db == "lift don't exists.":
                            info = {
                                "lift": lift_name_defects,
                                "defects": row["defects"],
                                "ncr": row["ncr"],
                                "cod": row["cod"]
                                }
                            lifts_defects_for_fix.append(info)
                        else:
                            # Insert data into table defect
                            lift_id = lift.get_lift_id_by_name(fix_lift_name)
                            defect.insert_defect(lift_id, row["icl_found"], correct_defects,correct_ncr, correct_cod)

                elif "skip" == correct_lift_name:
                    pass
                else:
                    # Insert data into table defect
                    lift_id = lift.get_lift_id_by_name(correct_lift_name)
                    defect.insert_defect(lift_id, row["icl_found"], correct_defects, correct_ncr, correct_cod)
            else:

                # Search lift in database
                lift_db = lift.get_lift_name_by_name(lift_name_defects)
                if lift_db == "lift don't exists.":
                    info = {
                        "lift": lift_name_defects,
                        "defects": row["defects"],
                        "ncr": row["ncr"],
                        "cod": row["cod"]
                    }
                    lifts_defects_for_fix.append(info)
                else:
                    # insert data into table defect
                    lift_id = lift.get_lift_id_by_name(lift_name_defects)
                    defect.insert_defect(lift_id, row["icl_found"], row["defects"], row["ncr"], row["cod"])

    print("Check the following lifts because don't match lift name in database: ")

    for item in lifts_defects_for_fix:
        print(f"Lift: {item['lift']}, defects: {item['defects']}, NCR: {item['ncr']}, COD: {item['cod']}")
    print(f"\nTotal lifts names to be fixed: {len(lifts_defects_for_fix)}")

    # Insert Data in Equipment
    equipment_file_path = Path(EQUIPMENT_FOLDER) / "equipment.csv"
    equipment_file = read_csv(equipment_file_path)
    for item in equipment_file:
        equipment_name = item["name"]
        equipment_type = item["type"]
        equipment.insert_equipment(equipment_name, equipment_type)
    # equipment.insert_equipment("BTB", "fixed")
    # equipment.insert_equipment("Telebelt", "mobile")
    # equipment.insert_equipment("Pump", "mobile")
    # equipment.insert_equipment("Rotec", "mobile")

    # save_csv(lifts_defects_for_fix,["lift","defects","ncr","cod"],"lifts_defects_for_fix.csv")
    
    ######################################################################################################
    # CDS (Create Table CDS and CDSLIFT - To break many to many relationship)
    
    # Read CDS csv file
    cds_filename = "cds_lifts_to_db.csv"
    full_cds_file_path = Path(CDS_FOLDER) / cds_filename
    cds_data = read_csv(full_cds_file_path)
    
    cds_report_data = []
    for item in cds_data:
        info = {}
        # CDS Report DATA
        info["report"] = item["report"]
        info["qty_equipment"] = item["qty_equipment"]
        info["volume"] = item["volume"]
        info["concrete_start"] = item["concrete_start"]
        info["concrete_finish"] = item["concrete_finish"]
        info["duration"] = item["duration"]
        info["calc_duration"] = item["calc_duration"]
        info["rate"] = item["rate"]
        info["calc_rate"] = item["calc_rate"]
        info["source"] = item["type"]
        
        if len(cds_report_data) == 0:
            cds_report_data.append(info)
        else:
            # Check if the dictionary alredy exists in the list
            duplicated = [x for x in cds_report_data if x == info]
            if len(duplicated) == 0:
                cds_report_data.append(info)
        
    # Insert CDS Report in table CDS
    cds_report_data_list = list(cds_report_data)
    for item in cds_report_data_list:
        cds.insert_cds(item["report"], item["qty_equipment"], item["volume"], item["concrete_start"],
                       item["concrete_finish"], item["duration"], item["calc_duration"],
                       item["rate"], item["calc_rate"],item["source"])
        
    # Create Table CDSLift
    for item in cds_data:
        report = item["report"]
        report_id = cds.get_report_id_by_name(report)
        lift_reported = item["lift"]
        lift_reported_id = lift.get_lift_id_by_name(lift_reported)
        cds_lift.insert_cdslift(report_id, lift_reported_id)
        
    print("CDS Values inserted successfully...")
        
        
    
            
        

    # Insert data in CRA table (TODO)
    ## Read CRA file
    # Pacific
    # cra_filename = "CRA_equipment.csv"
    # full_cra_file_path = Path(CRA_FOLDER) / cra_filename
    # cra_data = read_csv(full_cra_file_path)

    # for item in cra_data:
    #     site_abr = "P"
    #     # Get site id
    #     site_id = site.get_site_id_by_abr(site_abr)
    #     lift_name_cra = item["WBS Name"]
    #     # Fix lift name
    #     lift_name_cra = f"P{lift_name_cra.replace('-','')}"
    #     for struct in allowed_structures:
    #         if struct in lift_name_cra:
    #             lift_db = lift.get_lift_name_by_name(lift_name_cra)
    #             if lift_db == "lift don't exists.":
    #                 lifts_cra_for_fix.append(lift_name_cra)
    #             else:
    #                 # Get lift_id
    #                 lift_id = lift.get_lift_id_by_name(lift_name_cra)
    #     equipment_name = item["Resource Name"]
    #     # Get start_date
    #     start_date = item["Start"]
    #     # Fix start_date to match DB date format
    # for item in lifts_cra_for_fix:
    #     print(item)
    # print(f"Lifts in CRA for fix: {len(lifts_cra_for_fix)}")

    # Table NCNs
    # Read NCN files
    # full_path_ncn_file = Path(NCN_FOLDER) / "ncns.csv"
    # ncn_data = read_csv(full_path_ncn_file)
    # for item in ncn_data:
    #     # print(item)
    #     # Get site id
    #     site_abr = item["site"]
    #     site_id = site.get_site_id_by_abr(site_abr)
    #     # Get structure id
    #     structure_abr = item["structure"]
    #     structure_id = structure.get_structure_id_by_abr(structure_abr)
    #     # Get lift_id
    #     lift_name = item["lift"]
    #     lift_id = lift.get_lift_id_by_name(lift_name)
    #     # Get number
    #     ncn_number = item["number"]
    #     # Get title
    #     ncn_title = item["Title"]
    #     # Get date
    #     ncn_date = item["Date"]
    #     if structure_abr in allowed_structures:
    #         ncn.insert_ncn(site_id, structure_id, lift_id, ncn_number, ncn_title, ncn_date)


if __name__ == "__main__":
    main()