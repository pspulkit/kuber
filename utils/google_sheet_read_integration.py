import gspread
import pandas as pd

gc = gspread.service_account(filename='../project-100cr-7db0f1dfb28b.json')

# Open the Google Sheet by title
sh = gc.open("DeCoders Stock Trading Report")

# Specify the worksheet by title
worksheet_title = 'quant-volume-shockers-trends'
worksheet = sh.worksheet(worksheet_title)

# Get all records from the worksheet
records = worksheet.get_all_records()

# Convert the records to a DataFrame
df = pd.DataFrame(records)

# Display the DataFrame
print(df)
