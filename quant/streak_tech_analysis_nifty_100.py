import pandas as pd
import requests
import json
import os
from datetime import datetime
from io import StringIO
import gspread

url = "https://mo.streak.tech/api/tech_analysis_multi/"

list = [
    "NSE_COALINDIA", "NSE_TATACONSUM", "NSE_UPL", "NSE_HDFCBANK", "NSE_AXISBANK",
    "NSE_BAJAJ-AUTO", "NSE_ULTRACEMCO", "NSE_TITAN", "NSE_HDFCLIFE", "NSE_SBILIFE",
    "NSE_SBIN", "NSE_ASIANPAINT", "NSE_BRITANNIA", "NSE_KOTAKBANK", "NSE_HINDUNILVR",
    "NSE_LT", "NSE_WIPRO", "NSE_HEROMOTOCO", "NSE_DRREDDY", "NSE_INDUSINDBK", "NSE_HDFC",
    "NSE_CIPLA", "NSE_ICICIBANK", "NSE_SUNPHARMA", "NSE_RELIANCE", "NSE_INFY", "NSE_M&M",
    "NSE_BAJFINANCE", "NSE_DIVISLAB", "NSE_SHREECEM", "NSE_ONGC", "NSE_BHARTIARTL",
    "NSE_NESTLEIND", "NSE_HINDALCO", "NSE_GRASIM", "NSE_TATASTEEL", "NSE_BAJAJFINSV",
    "NSE_TATAMOTORS", "NSE_HCLTECH", "NSE_ITC", "NSE_NTPC", "NSE_EICHERMOT", "NSE_TCS",
    "NSE_BPCL", "NSE_POWERGRID", "NSE_IOC", "NSE_ADANIPORTS", "NSE_JSWSTEEL", "NSE_MARUTI",
    "NSE_TECHM", "NSE_ADANIGREEN", "NSE_ADANITRANS", "NSE_ABBOTINDIA", "NSE_PGHH", "NSE_MARICO",
    "NSE_INDUSTOWER", "NSE_COLPAL", "NSE_HAVELLS", "NSE_PIDILITIND", "NSE_ALKEM", "NSE_JUBLFOOD",
    "NSE_SIEMENS", "NSE_YESBANK", "NSE_VEDL", "NSE_MCDOWELL-N", "NSE_LTI", "NSE_BERGEPAINT",
    "NSE_ICICIGI", "NSE_DMART", "NSE_AMBUJACEM"
]

headers = {
    'Content-Type': 'application/json'
}

df = pd.DataFrame()
for s in range(0, len(list), 20):
    payload = json.dumps({
        "time_frame": "day",
        "stocks": list[s:s + 20],
        "user_broker_id": "UZ4984"
    })
    response = requests.request("POST", url, headers=headers, data=payload)
    data = json.loads(response.text)['data']
    df = df._append(pd.read_json(StringIO(json.dumps(data))).transpose())

indicators = [
    'adx', 'awesome_oscillator', 'cci', 'change', 'close',
    'ema10', 'ema100', 'ema20', 'ema200', 'ema30', 'ema5', 'ema50', 'hma',
    'ichimoku', 'loss_amt', 'loss_signals', 'macd', 'macdHist', 'momentum',
    'rec_adx', 'rec_ao', 'rec_cci', 'rec_ichimoku', 'rec_macd', 'rec_mom',
    'rec_rsi', 'rec_stochastic_k', 'rec_stochastic_rsi_fast', 'rec_ult_osc', 'rec_willR', 'rsi', 'signals',
    'sma10', 'sma100', 'sma20', 'sma200', 'sma30', 'sma5', 'sma50',
    'state', 'status', 'stoch_rsi_fast', 'stochastic_k', 'ult_osc', 'vwma', 'willR', 'win_amt', 'win_pct', 'win_signals'
]

print("started")

# Get today's date
df['date'] = pd.Timestamp(datetime.today().strftime('%Y-%m-%d'))

result = df.query('rsi  < 30 or rsi  > 70')
output_filename = os.path.abspath("../reports/daily/streak-technical-indicators-nifty100.csv")
result.to_csv(output_filename)

# df = df.reset_index(drop=True)
df_reset = df.reset_index(drop=False)
gsheet = df_reset.astype(str)
gsheets = gspread.service_account(filename='../project-100cr-7db0f1dfb28b.json')
spreadsheet = gsheets.open('DeCoders Stock Trading Report')
worksheet = spreadsheet.worksheet('technical-indicators-nifty100')
worksheet.clear()

new_headers = gsheet.columns.tolist()
new_values = gsheet.values.tolist()
worksheet.update('A1', [new_headers])
worksheet.update('A2', new_values)

print("finished")
