from io import StringIO
import pandas as pd
import requests
import json
import os


# Function to load the configuration from a JSON file
def load_config(file_path=os.path.abspath('../../config.json')):
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config


configs = load_config()
finology_holdings = configs["finology"]["big_investors"]

headers = {'Content-Type': 'application/json'}

df = pd.DataFrame()
for k, v in finology_holdings.items():
    response = requests.get(v, headers=headers)
    temp = pd.read_html(StringIO(response.text))[0]
    temp['investor'] = k
    df = df._append(temp)

df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
df = df.sort_values(by=['COMPANY', 'investor'], ascending=[True, True])
desired_order = ['COMPANY', 'investor', 'ValueCr.', 'Sep 2023%', 'Jun 2023%', 'Mar 2023%', 'Dec 2022%', 'Sep 2022%']
df = df[desired_order]
# df.set_index(['COMPANY', 'investor'], inplace=True)
root_file_path = '//smart_money_tracker/reports/'
filename = 'investor-holding-finology-as-sept2023.csv'
df.to_csv(root_file_path + filename)
