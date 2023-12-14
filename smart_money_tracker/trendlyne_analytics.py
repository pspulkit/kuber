import http.client
import pandas as pd

conn = http.client.HTTPSConnection("trendlyne.com")
payload = ''
headers = {
  'Cookie': 'csrftoken=YmPXQerRU6jQlJwzGt8nYJebj82AICFCfngWJGMf5ETWvg2Rm6qey1HWIgzZhQyq'
}
conn.request("GET", "/portfolio/bulk-block-deals/", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
# pd.read_html(data.decode("utf-8"))[0]