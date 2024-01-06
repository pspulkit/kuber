import yfinance as yf

stock_symbol = 'TATAMOTORS.NS'
stock = yf.Ticker(stock_symbol)
stock_stats = stock.info
print(f"Stock Statistics for {stock_symbol}:")
print("====================================")

data = {}
for key, value in stock_stats.items():
    data[f"{key}"] = value

data
