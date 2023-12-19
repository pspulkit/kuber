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
investors_holdings = configs["stockedge"]["big_investors"]

base_dir = "../../reports/quarterly"
filename = 'investor-holding-stockedge-as-sept2023.csv'
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
        temp = pd.read_json(v.replace('GetParentClientBulkDeals', 'GetLatestShareHolderSecuritiesForClient'))

        if temp.size == 0:
            continue

        # Perform data cleaning using Pandas methods

        temp['Investor'] = k
        temp['holdings_quantity'] = pd.to_numeric(temp['NumberOfShares'], errors='coerce')
        # temp['holdings_as_of'] = datetime.strptime("2023-09-30", "%Y-%m-%d")
        temp['StockName'] = temp['SecurityName'].str.strip()
        temp['DateEndName'] = pd.to_datetime(temp['DateEndName'], format="%Y-%m")
        temp = temp.query('DateEndName > "2023-01-01"')
        temp = temp.sort_values(by=['StockName', 'Investor', 'DateEndName', 'holdings_quantity'],
                                ascending=[True, True, False, False])

        desired_order = ['Investor', 'StockName', 'DateEndName', 'SecurityID', 'Percentage', 'holdings_quantity',
                         'NumberOfShares', 'SecurityName', 'CategoryID', 'CategoryName', 'SecuritySlug']

        temp = temp.drop(['ClientID', 'ClientName', 'DateEnd'], axis=1)
        temp = temp[desired_order]

        # Append to the file in append mode
        temp.to_csv(output_file_path, mode='a', header=is_header, index=False)
        is_header = False

except Exception as e:
    print(f"An error occurred: {str(e)}")
