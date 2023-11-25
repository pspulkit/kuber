import pandas as pd

# purchases or sells more than 0.5% of a company’s equity shares through a single transaction
# may impact the stock’s price and overall market sentiment
# happen during the normal trading window provided by the broker, and it is a market-driven deal

bulk_deals = pd.DataFrame()
page = 1
while True:
    df = pd.read_json(
        f"https://api.stockedge.com/Api/DailyDashboardApi/GetLatestBulkDeals?page={page}&pageSize=100&lang=en")
    bulk_deals = bulk_deals._append(df)
    if df['Date'][99].date() < (pd.to_datetime('today') - pd.DateOffset(months=6)).date():
        break
    page += 1

bulk_deals['DealValue'] = (bulk_deals['Quantity'] * bulk_deals['Price']) / (1000 * 1000 * 10)
bulk_deals['DealValue'] = pd.to_numeric(bulk_deals['DealValue'], errors='coerce')
bulk_deals.sort_values('DealValue', ascending=False)
bulk_deals.to_csv(f"stockedge-bulk-deals-{pd.to_datetime('today').date()}.csv")
