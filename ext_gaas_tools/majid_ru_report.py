import requests
import xlsxwriter

from common.date_tool import timestamp_to_string, current_text_month, current_text_year
from config import output_location


def fetch_data_from_gaas():
    """Fetch RU from GaaS API"""
    print('Fetching data from GaaS')

    url = "http://localhost:8000/api/v1/gdnrubyclients/?oldru"
    response = requests.request("GET", url)
    return response.json()


def output_data_to_excel(data):
    print('Building Excel File')
    # Some var setup for names and shits
    workbook_name = r'majid_ru_report_%s' % timestamp_to_string()
    worksheet_name = r'%s %s' % (current_text_month(), current_text_year())
    output_path = r'%s\%s.xlsx' % (output_location, workbook_name)

    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(output_path)
    worksheet = workbook.add_worksheet(worksheet_name)

    # Some styles format
    worksheet.set_column('A:A', 22)
    worksheet.set_column('B:C', 10)
    worksheet.set_column('D:D', 32)
    green_bold_bg = workbook.add_format({'bold': True, 'bg_color': '#a0c29f'})
    orange_bold_bg = workbook.add_format({'bold': True, 'bg_color': '#ffa26b'})
    green_bold_bg.set_text_wrap()
    orange_bold_bg.set_text_wrap()

    # Write headers
    worksheet.write('A1', 'Client ID', green_bold_bg)
    worksheet.write('B1', 'Service ID (RU Code)', orange_bold_bg)
    worksheet.write('C1', 'Current Month Volume', orange_bold_bg)
    worksheet.write('D1', 'CIE Name', orange_bold_bg)

    # Start from the first cell. Rows and columns are zero indexed.
    # Ref. A1 is (0, 0)
    row = 1
    col = 0

    # Iterate over the data and write it out row by row
    for mandate, service, value, client in data:
        worksheet.write(row, col, mandate)
        worksheet.write(row, col + 1, service)
        worksheet.write(row, col + 2, value)
        worksheet.write(row, col + 3, client)
        row += 1

    workbook.close()
    print('Output completed see\t%s' % output_path)


def format_to_excel_data(data):
    return [[row['mandate'], row['service'], float(row['value']), row['client']] for row in data if
            float(row['value']) > 0 and row['mandate'].casefold() != 'ferme']


def main():
    data = fetch_data_from_gaas()
    excel_like_data = format_to_excel_data(data=data)
    output_data_to_excel(data=excel_like_data)


def tester():
    pass


if __name__ == "__main__":
    import doctest

    doctest.testmod(main())
