import json


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
