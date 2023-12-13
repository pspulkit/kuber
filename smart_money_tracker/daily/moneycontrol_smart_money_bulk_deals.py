import pandas as pd
import json
import os


# Function to load the configuration from a JSON file
def load_config(file_path=os.path.abspath('../../config.json')):
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config


def create_reports_dir(base_dir="../../reports/"):
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    if not os.path.exists(base_dir + "/daily"):
        os.makedirs(base_dir + "/daily")


configs = load_config()
investors_bulk_deals = configs["moneycontrol"]["big_investors"]

create_reports_dir()
holdings = pd.read_csv(os.path.abspath('../../reports/quarterly/investor-holding-moneycontrol-as-sept2023.csv'))
output_filename = os.path.abspath("../../reports/daily/moneycontrol-bulk-deals-latest.csv")

deals_df = pd.DataFrame()
for k, v in investors_bulk_deals.items():
    temp = pd.read_html(v + '/bulk-block-deals')[0]
    temp['investor'] = k
    try:
        temp['bulk_deal_date'] = pd.to_datetime(temp['Date'], format='mixed')
    except ValueError as e:
        print(e)
    temp['bulk_deal_value'] = (temp['Quantity'] * temp['Avg Price']) / (1000 * 1000 * 10)  # in cores
    deals_df = deals_df._append(temp)

df = pd.merge(holdings, deals_df, on=['investor', 'Stock Name'], how='right')
df['profit_loss'] = df['Avg Price'] - df['holding_average_price']
desired_order = ['Stock Name', 'investor', 'Action', 'bulk_deal_date', 'bulk_deal_value', 'Deal type', 'Quantity',
                 'Avg Price', 'Quantity Held', 'holding_average_price', 'profit_loss', 'Holder Name', 'holdings_change']
df = df[desired_order]
df = df.sort_values(by=['bulk_deal_date', 'Stock Name'], ascending=[False, True])
df.set_index(['Stock Name'], inplace=True)
df.to_csv(output_filename)
