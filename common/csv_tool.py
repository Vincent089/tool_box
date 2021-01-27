import csv
from datetime import datetime


def build_csv_with_headers(file_name, file_headers, file_rows):
    """
    Output into _file_output folder a csv build from file_rows and mapped with file_headers
    The output file will have the given name and a time stamp to avoir overwriting csv with the same name
    :param file_name:
    :param file_headers:
    :param file_rows:
    :return:
    """
    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

    with open('../_file_output/%s_%s.csv' % (file_name, str(timestamp)), encoding='utf8', mode='w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=file_headers, delimiter=';')
        writer.writeheader()
        writer.writerows(file_rows)

    print('Output completed --> %s_%s.csv' % (file_name, str(timestamp)))


def build_list_from_csv(file_location, delimiter):
    """
    Open the csv file provided in file_location and use the delimiter to separate columns and return a list out of it
    :param file_location:
    :param delimiter:
    :return:
    """
    with open(file_location, mode='r', encoding='utf8') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=delimiter)
        result = list(csv_reader)

    return result


def load_file(file_location):
    """
    Simply loading reading a text file location and returning its content
    :param file_location:
    :return:
    """
    with open(file_location, encoding='utf8') as file:
        print('Reading File\t%s' % file.name)
        contents = file.read()

    return contents
