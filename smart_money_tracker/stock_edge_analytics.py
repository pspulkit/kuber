import pandas as pd
import requests
import json
from io import StringIO

# To get all the symbols of Nifty50
nifty50 = pd.read_html('https://en.wikipedia.org/wiki/NIFTY_50#Constituents')
symbols = nifty50[2]['Symbol'].tolist()
mo_streak = []

for s in symbols:
    mo_streak.append(f"NSE_{s}")

headers = {'Content-Type': 'application/json'}
mo_streak_url = "https://mo.streak.tech/api/tech_analysis_multi/"
df_tech_indicators = pd.DataFrame()
for s in range(0, len(mo_streak), 20):
    payload = json.dumps({
        "time_frame": "day",
        "stocks": mo_streak[s:s + 20],
        "user_broker_id": "UZ4984"
    })
    response = requests.request("POST", mo_streak_url, headers=headers, data=payload)
    data = json.loads(response.text)['data']
    df_tech_indicators = df_tech_indicators._append(pd.read_json(StringIO(json.dumps(data))).transpose())

df_tech_indicators
# shares with a minimum value of Rs.10 crores between two known parties at an agreed-upon price
# executed separately through a single transaction on the special “Block Deal window” between 9.15 AM and 9.50 AM
# pre agreed price - less instant impact on market

# block_deals = pd.read_json(
#     'https://api.stockedge.com/Api/DailyDashboardApi/GetLatestBlockDeals?page=1&pageSize=10&lang=en')

# purchases or sells more than 0.5% of a company’s equity shares through a single transaction
# may impact the stock’s price and overall market sentiment
# happen during the normal trading window provided by the broker and it is a market-driven deal
bulk_deals = pd.read_json(
    'https://api.stockedge.com/Api/DailyDashboardApi/GetLatestBulkDeals?page=1&pageSize=100&lang=en')
bulk_deals['DealValue'] = (bulk_deals['Quantity'] * bulk_deals['Price']) / (1000 * 1000 * 10)
bulk_deals['DealValue'] = pd.to_numeric(bulk_deals['DealValue'], errors='coerce')
bulk_deals.sort_values('DealValue', ascending=False)
bulk_deals.head(5)
