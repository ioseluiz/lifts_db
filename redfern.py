from main import read_csv
from pathlib import Path
from db.lift import get_lift_id_by_name
import os

ROOT_FOLDER = os.getcwd()
CDS_FOLDER = Path(ROOT_FOLDER) /"CDS"

def main():

    # Read csv file
    cds_filename = "cds_redfern_request.csv"
    full_cds_file_path = Path(CDS_FOLDER) / cds_filename
    cds_data = read_csv(full_cds_file_path)
    
    lifts_not_in_db = []
    
    for item in cds_data:
        if not get_lift_id_by_name(item["lift"]):
            print(item["lift"])
        else:
            pass
    

if __name__ == "__main__":
    main()