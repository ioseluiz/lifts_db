from pathlib import Path
import os
import csv
from db import lift

ROOT_FOLDER = os.getcwd()
CRA_FOLDER = Path(ROOT_FOLDER) / "CRA"

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
    # Read csv file
    cra_rebar_pac_file = Path(CRA_FOLDER) / "PAC_CRA_Rebar.csv"
    cra_rebar_data = read_csv(cra_rebar_pac_file)
    data = []
    not_found = []
    for item in cra_rebar_data:
        info = {}
        info['lift'] = item['Activity ID']
        info['lift'] = info['lift'][:-3]
        info['lift'] = f"P{info['lift'].replace('-','')}"


        # Check if lift exists in database
        lift_id = lift.get_lift_id_by_name(info['lift'])
        if not lift_id:
            not_found.append({"lift": info['lift'], "rebar_units": item['Budgeted Units']})
        else:
            info['rebar_units'] = item['Budgeted Units']
            data.append(info)
        # print(f"Lift: {info['lift']}, Rebar Units: {info['rebar_units']}")

    headers = ["lift", "rebar_units"]
    save_csv(data, headers, "data_cra_rebar_found.csv")
    save_csv(not_found, headers, "data_cra_rebar_not_found.csv")


    



if __name__ == "__main__":
    main()