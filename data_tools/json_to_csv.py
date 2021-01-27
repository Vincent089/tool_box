import json
import collections
import csv
from datetime import datetime

file_rows = list()


def print_dict_items(elements):
    for key, value in elements.items():

        # Recursive call if inner element is a dictionary as well
        if isinstance(value, collections.Mapping):
            print_dict_items(value)

        # Sub function to validate inner list elements
        # ultimately this is a recursive call as well, see function comment
        if isinstance(value, collections.Sequence):
            print_list_values(value)

        if key_to_print:
            if key in file_headers:
                print(key, ' = ', value)
        else:
            print(key, ' = ', value)


# Validate if values is dictionary, if yes call print_dict_items with his content
def print_list_values(values):
    for value in values:
        if isinstance(value, collections.Mapping):
            print_dict_items(value)


def read_dict(element, append_content):
    content = append_content

    for key, value in element.items():

        # Recursive call if inner value is a dictionary as well
        if isinstance(value, collections.Mapping):
            content = read_dict(value, content)

        if isinstance(value, list):
            for item in value:

                # Recursive call if inner value is a dictionary as well
                if isinstance(item, collections.Mapping):

                    # only the deepest array will return a value that will be added to the global file row array
                    # as any other results are trapped in a contact loop to bring up the floor of the JSON into one lvl
                    result = read_dict(item, dict())

                    # Add result to the global file row array
                    if result:
                        file_rows.append(result)

        if key in file_headers:
            content.update({key: value})

    return content


def build_csv():
    doc_name = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    with open('../_file_output/converted_json_' + str(doc_name) + '.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=file_headers, delimiter=';')
        writer.writeheader()
        writer.writerows(file_rows)


def console_output():
    with open(file_location) as jsonFile:
        print('\nFile data acquired')
        print('Outputting to screen...')

        data = json.load(jsonFile)

    print_dict_items(data)


def file_output():
    with open(file_location) as jsonFile:
        print('\nFile data acquired')
        print('Outputting to file...')

        data = json.load(jsonFile)

    read_dict(data, dict())
    build_csv()


# Entry point
if __name__ == "__main__":
    # user entry
    file_location = input('Enter your json file path : ')
    key_to_print = input('Enter the keys you wish to export (e.g.: A, B, C)  : ')

    # file building vars
    file_headers = key_to_print.replace(' ', '').split(',')

    # Uncomment to see result in python console
    # console_output()

    # Comment to avoid csv creation
    file_output()

    # Uncomment to see result in python console
    # for row in file_rows:
    #     print(row)

    print('\nScript completed !')
