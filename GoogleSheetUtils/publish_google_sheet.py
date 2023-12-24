import gspread
import pandas as pd

new_data_df = pd.DataFrame({
    'Column1': [4, 5, 6],
    'Column2': ['D', 'E', 'F'],
    'Column3': [9.1, 7.3, 5.8]
})


def publish_to_google_sheet(google_sheet):
    # Create a Google Sheets service object.
    gsheets = gspread.service_account(filename='../project-100cr-7db0f1dfb28b.json')

    # Open the spreadsheet you want to update.
    spreadsheet = gsheets.open('DeCoders Stock Trading Report')

    # Get the worksheet you want to update.
    worksheet = spreadsheet.worksheet('quant-volume-shockers-trends')
    worksheet.clear()

    new_headers = new_data_df.columns.tolist()
    new_values = new_data_df.values.tolist()

    worksheet.update('A1', [new_headers])
    worksheet.update('A2', new_values)
