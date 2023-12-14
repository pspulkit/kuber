import pandas as pd
import requests
import os

print("started")

# Fetch data for bullish trend
url_bullish = "https://api.streak.tech/screener/?screener_uuid=bdcec4cf-4761-4cfe-b129-7f6a16a8c910&sample=true&broker=zerodha"
response_bullish = requests.get(url_bullish)
data_bullish = response_bullish.json()
bullish_trend = pd.DataFrame(data_bullish['screener_result'])
bullish_trend['indicator'] = 'volume-gainers-with-bullish-trend'

# Fetch data for bearish trend
url_bearish = "https://api.streak.tech/screener/?screener_uuid=0c832bc7-eb98-4174-ae0c-1eaa06807e3c&sample=true&broker=zerodha"
response_bearish = requests.get(url_bearish)
data_bearish = response_bearish.json()
bearish_trend = pd.DataFrame(data_bearish['screener_result'])
bearish_trend['indicator'] = 'volume-gainers-with-bearish-trend'

merged_df = pd.concat([bullish_trend, bearish_trend])
# merged_df.sort_values(by=['indicator','seg_sym'], ascending=[False, True])
merged_df.set_index(['seg_sym'], inplace=True)

output_filename = os.path.abspath("../reports/daily/streak-volume-deals-latest.csv")
merged_df.to_csv(output_filename)

print("finished")
