import pandas as pd
from datetime import datetime
import json
import os


# Function to load the configuration from a JSON file
def load_config(file_path=os.path.abspath('../../config.json')):
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config


configs = load_config()
investors_holdings = configs["moneycontrol"]["big_investors"]

base_dir = "../../reports/quarterly"
filename = 'investor-holding-moneycontrol-as-sept2023.csv'
output_file_path = os.path.abspath(os.path.join(base_dir, filename))

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

        temp['holdings_as_of'] = datetime.strptime("2023-09-30", "%Y-%m-%d")
        temp['Stock Name'] = temp['Stock Name'].strip()
        temp['holding_average_price'] = temp['holdings_value'] * 100 * 100 * 1000 / temp['holdings_quantity']
        temp = temp.sort_values(by=['Stock Name', 'investor', 'holdings_change', 'holdings_value'],
                                ascending=[True, True, False, False])

        temp = temp.dropna(subset=['holdings_change'])

        # Append to the file in append mode
        temp.to_csv(output_file_path, mode='a', header=is_header, index=False)
        is_header = False

except Exception as e:
    print(f"An error occurred: {str(e)}")
