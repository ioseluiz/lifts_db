from pathlib import Path
from datetime import datetime
import os
import csv
from db import lift, pour

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
    
def get_lift_min_actual_start(list_lifts):
    # print(list_lifts)
    actual_start_datetime = datetime(year=2017, month=1, day=1)
    for item in list_lifts:
        actual_start = pour.get_lift_actual_start(item[0])
        # print(f"Lift: {item[1]} Actual start: {actual_start}")
        actual_start = datetime.strptime(actual_start, "%m/%d/%Y")
        if actual_start < actual_start_datetime:
            actual_start_datetime = actual_start

    return datetime.strftime(actual_start_datetime, "%m/%d/%Y") 



def main():
    # Read csv file
    cra_rebar_pac_file = Path(CRA_FOLDER) / "PAC_CRA_Rebar.csv"
    cra_rebar_data = read_csv(cra_rebar_pac_file)
    data = []
    not_found = []
    for item in cra_rebar_data:
        info = {}
        info['original_lift'] = item['Activity ID']
        info['lift'] = item['Activity ID']
        info['lift'] = info['lift'][:-3]
        # Check if conduits or crossunder lifts
        abr_structures = ["UC", "MC","LC"]
        if info['lift'][0:2] in abr_structures:
            info['lift'] = info['lift'][2:]
        
        if info['lift'][0:5] == "LE-CC":
             info['lift'] = info['lift'][2:]

        if info['lift'][0:5] == "LW-CC":
             info['lift'] = info['lift'][2:]

        if info['lift'][0:5] == "UE-CC":
             info['lift'] = info['lift'][2:]

        if info['lift'][0:5] == "UW-CC":
             info['lift'] = info['lift'][2:]

        if info['lift'][0:5] == "ME-CC":
             info['lift'] = info['lift'][2:]

        if info['lift'][0:5] == "MW-CC":
             info['lift'] = info['lift'][2:]


        info['lift'] = f"P{info['lift'].replace('-','')}"
        info['lift'] = info['lift'].replace(' ','')


        # Check if lift exists in database
        lift_id = lift.get_lift_id_by_name(info['lift'])
        if not lift_id:
            not_found.append({"original_lift": info['original_lift'], "lift": info['lift'], "rebar_units": item['Budgeted Units']})
        else:
            info['rebar_units'] = item['Budgeted Units']
            # Get actual pour data
            actual_start = pour.get_lift_actual_start(lift_id)
            info['actual_start'] = actual_start
            data.append(info)
        # print(f"Lift: {info['lift']}, Rebar Units: {info['rebar_units']}")

   


    # Check if a lift not found is divided
    # print('Lifts not found:\n')
    new_not_found = []
    for x in not_found:
        # print(f"Not found list: {x['original_lift']}, {x['lift']}")
        info_not_found = {}
        info_not_found['original_lift'] = x['original_lift']
        info_not_found['lift'] = x['lift']
        info_not_found['rebar_units'] = x['rebar_units']
        lift_not_found_list = lift.get_lifts_that_contain_name(x['lift'])
        if len(lift_not_found_list) > 0:
            actual_start_lift = get_lift_min_actual_start(lift_not_found_list)
            info_not_found['actual_start'] = actual_start_lift
            data.append(info_not_found)
            not_found.remove({'original_lift': x['original_lift'], 'lift': x['lift'], 'rebar_units': x['rebar_units']})
        else:
            print(info_not_found['lift'])
            # new_not_found.append({'original_lift': x['original_lift'], 'lift': x['lift'], 'rebar_units': x['rebar_units']})



    headers_found = ["original_lift","lift", "rebar_units", "actual_start"]
    headers_not_found = ["original_lift","lift", "rebar_units"]

    # print(f'Cantidad Not Found: {len(not_found)}')
    save_csv(data, headers_found, "data_cra_rebar_found.csv")

    save_csv(not_found, headers_not_found, "data_cra_rebar_not_found.csv")


    



if __name__ == "__main__":
    main()