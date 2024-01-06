from io import StringIO
import pandas as pd
import requests
import json
import os
import gspread


# Function to load the configuration from a JSON file
def load_config(file_path=os.path.abspath('../../config.json')):
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config


def perform_request(config_path):
    finology_holdings = load_config(config_path)["finology"]["big_investors"]

    df = pd.DataFrame()
    for k, v in finology_holdings.items():
        response = requests.get(v, headers={'Content-Type': 'application/json'})
        temp = pd.read_html(StringIO(response.text))[0]
        temp['Investor'] = k
        df = df._append(temp)

    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    df = df.drop(['S.No.'], axis=1)

    desired_order = [
        'COMPANY', 'Investor', 'ValueCr.', 'Dec 2023%', 'Sep 2023%', 'Jun 2023%', 'Mar 2023%', 'Dec 2022%', 'Sep 2022%'
    ]
    df = df.sort_values(by=['COMPANY', 'Investor', 'ValueCr.'], ascending=[True, False, True])
    update_google_sheet(df[desired_order])


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


def update_to_csv(data):
    base_dir = "../../reports"
    filename = 'investor-holding-finology-as-latest-quarter.csv'
    output_file_path = os.path.abspath(os.path.join(base_dir, filename))
    print(f"output_file_path_moneycontrol: {output_file_path}")
    data.to_csv(output_file_path)


if __name__ == '__main__':
    perform_request(os.path.abspath('../../config.json'))
