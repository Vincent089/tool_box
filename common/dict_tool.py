import collections


def print_dict_items(elements):
    for key, value in elements.items():

        # Recursive call if inner element is a dictionary as well
        if isinstance(value, collections.Mapping):
            print_dict_items(value)

        # Sub function to validate inner list elements
        # ultimately this is a recursive call as well, see function comment
        if isinstance(value, collections.Sequence):
            print_list_values(value)
        else:
            print(key, ' = ', value)


# Validate if values is dictionary, if yes call print_dict_items with his content
def print_list_values(values):
    for value in values:
        if isinstance(value, collections.Mapping):
            print_dict_items(value)
