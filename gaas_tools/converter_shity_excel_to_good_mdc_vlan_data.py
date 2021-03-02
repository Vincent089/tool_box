import re
from common.csv_tool import build_list_from_csv
from common.date_tool import timestamp_to_string

if __name__ == "__main__":
    # raw extract from the mdc vlan excel file, minus manual work to remove title doubling and empty lines
    file_location = r'C:\Users\vincent.corriveau\Documents\Gaas\mdc_vlan_20201019.csv'

    # regex match vlan name conventions of "IP address" + / + "mask" (between 20 - 21) + "_" + any char chain with it
    reg = re.compile(r'(?:1?\d?\d|2[0-4]\d|25[0-5])(?:\.(?:1?\d?\d|2[0-4]\d|25[0-5])){3}/(?:2?\d|3[0-1])_?\w*')

    data = build_list_from_csv(file_location=file_location,
                               delimiter='\t')

    # only take the line if there is something in status column
    active_vlans = filter(lambda data_row: data_row['status'].strip().lower() != '', data)
    data = list(active_vlans)

    with open('../_file_output/%s_%s.txt' % ('mdc_vlan', timestamp_to_string()), "w") as file:
        for row in data:
            number = row['number']
            name = row['status'] if reg.match(row['status']) else row['name']

            file.write('%s%s%s\n' % (number.ljust(5), 'mdc;', name[:32]))
