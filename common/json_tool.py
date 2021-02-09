import json

from common.date_tool import timestamp_to_string
from config import output_location


def load_file(file_location: str):
    """
    Load a json file into the script
    :param file_location:
    :return:
    """
    with open(file_location) as jsonFile:
        print('\nFile data loaded')

        data = json.load(jsonFile)

    return data


def output_to_json_file(file_name, dict_data: dict):
    timestamp = timestamp_to_string()

    with open('%s\%s_%s.json' % (output_location, file_name, timestamp), 'w') as file:
        file.write(json.dumps(dict_data))

    print('Output completed --> %s_%s.json' % (file_name, str(timestamp)))
