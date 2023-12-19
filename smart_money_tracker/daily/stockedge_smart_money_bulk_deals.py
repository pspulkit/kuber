import pandas as pd
import json
import os


# purchases or sells more than 0.5% of a company’s equity shares through a single transaction
# may impact the stock’s price and overall market sentiment
# happen during the normal trading window provided by the broker, and it is a market-driven deal

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
investors_bulk_deals = configs["stockedge"]["big_investors"]

output_filename = os.path.abspath("../../reports/daily/stockedge-bulk-deals-latest.csv")
deals_df = pd.DataFrame()

for k, v in investors_bulk_deals.items():
    temp = pd.read_json(v)
    temp['investor'] = k
    try:
        temp['bulk_deal_date'] = pd.to_datetime(temp['Date'], format='mixed')
    except ValueError as e:
        print(e)
    temp['bulk_deal_value'] = (temp['Quantity'] * temp['Price']) / (1000 * 1000 * 10)  # in cores
    deals_df = deals_df._append(temp)

# df = pd.merge(holdings, deals_df, on=['investor', 'Stock Name'], how='right')
df = deals_df
# df['profit_loss'] = df['Avg Price'] - df['holding_average_price']
df['Stock Name'] = df['SecurityName']
df = df.sort_values(by=['bulk_deal_date', 'SecurityID'], ascending=[False, True])
desired_order = ['Stock Name', 'investor', 'BuySellName', 'DealTypeName', 'Price', 'Quantity', 'Date',
                 'ClientName', 'ExchangeName', 'SecurityID', 'bulk_deal_value', 'ID']
df = df[desired_order]
df.set_index(['Stock Name'], inplace=True)
df.to_csv(output_filename)
