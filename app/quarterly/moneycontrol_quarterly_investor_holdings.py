import pandas as pd
from datetime import datetime
import json
import os
import gspread


# Function to load the configuration from a JSON file
def load_config(file_path=os.path.abspath('../../config.json')):
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config


def perform_request(config_path):
    configs = load_config(config_path)
    investors_holdings = configs["moneycontrol"]["big_investors"]

    base_dir = "../../reports"
    filename = 'investor-holding-moneycontrol-as-latest-quarter.csv'
    output_file_path = os.path.abspath(os.path.join(base_dir, filename))
    print(f"output_file_path_moneycontrol: {output_file_path}")

    try:
        # Ensure the directory exists
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
            print(f"Directory '{base_dir}' created.")

        # Delete existing file if it exists
        if os.path.exists(output_file_path):
            os.remove(output_file_path)

        is_header = True
        for k, v in investors_holdings.items():
            temp = pd.read_html(v + "/holdings")[0]

            # Perform data cleaning using Pandas methods
            temp['investor'] = k
            temp['holdings_value'] = pd.to_numeric(temp['Holding Value(Crs.)'], errors='coerce')
            temp['holdings_change'] = pd.to_numeric(temp['Change From Prev. Qtr.'], errors='coerce')
            temp['holdings_quantity'] = pd.to_numeric(temp['Quantity Held'], errors='coerce')

            temp = temp.drop(
                ['Unnamed: 7', 'Unnamed: 0', 'History', 'Holding(%)', 'Change From Prev. Qtr.', 'Holding Value(Crs.)'],
                axis=1)

            temp['holdings_as_of'] = datetime.strptime("2023-12-31", "%Y-%m-%d")
            temp['Stock Name'] = temp['Stock Name'].str.strip()
            temp['holding_average_price'] = temp['holdings_value'] * 100 * 100 * 1000 / temp['holdings_quantity']
            temp = temp.dropna(subset=['holdings_change'])
            temp = temp.sort_values(by=['Stock Name', 'investor', 'holdings_change', 'holdings_value'],
                                    ascending=[True, True, False, False])

            # Append to the file in append mode
            temp.to_csv(output_file_path, mode='a', header=is_header, index=False)
            is_header = False

    except Exception as e:
        print(f"An error occurred: {str(e)}")


def update_google_sheet(data):
    gsheet = data.astype(str)
    gsheets = gspread.service_account(filename='project-100cr-7db0f1dfb28b.json')
    spreadsheet = gsheets.open('DeCoders Stock Trading Report')
    worksheet = spreadsheet.worksheet('super-investors-quarterly-holdings')
    worksheet.clear()

    new_headers = gsheet.columns.tolist()
    new_values = gsheet.values.tolist()
    worksheet.update('A1', [new_headers])
    worksheet.update('A2', new_values)


if __name__ == '__main__':
    perform_request()
