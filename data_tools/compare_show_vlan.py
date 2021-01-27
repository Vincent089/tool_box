from common.csv_tool import load_file


def convert_content_to_dict(file_data):
    """
    Split a file data (very long string) into an array based on prompt return. Than map each row by vlan number and name
    and return it as a dict
    :param file_data:
    :return:
    """
    file_by_rows = file_data.split('\n')
    return {row[:5].strip(): row[5:].strip() for row in file_by_rows}


# Entry point
if __name__ == "__main__":
    file_locations = [r'C:\Users\vincent.corriveau\Documents\Workshop\tool_box\_file_input\mdc_fabric_vlan.txt',
                      r'C:\Users\vincent.corriveau\Documents\Workshop\tool_box\_file_input\mdc_old_core_vlan.txt']

    files = [load_file(location) for location in file_locations]
    mapped_files = [convert_content_to_dict(file_content) for file_content in files]

    analyse_content = {'index': None, 'content': None}
    i = 0

    while i < len(mapped_files):
        analyse_content = {'index': i,
                           'content': mapped_files[i].keys()}

        for content in mapped_files:
            saved_index = analyse_content['index']
            current_index = mapped_files.index(content)

            if saved_index != current_index:
                diff_list = list(set(analyse_content['content']).difference(content.keys()))

                # since we are dealing only with raw values in string in order to make it "number" order friendly
                # we have to convert them all to number before sorting the result
                number_list = [int(str_number) for str_number in diff_list]
                number_list.sort()

                print('\nComparing index %d with position %d' %
                      (saved_index, current_index))

                print(', '.join(map(str, number_list)))

        i = i + 1

print('\nScript completed !')
