import logging

import pymysql

from gaas_tools.models.vlan import Vlan


def load_vlan_from_file(file_path, delimiter=None, vlan_number_header_name='number', vlan_name_header_name='name'):
    from common.csv_tool import load_file_with_header
    # gets the file content with header ref
    file_content = load_file_with_header(file_path=file_path, delimiter=delimiter)
    # init each row as a Vlan TODO: create a reference to the file instead of hard code core id
    vlans = convert_file_data_to_vlans(file_data=file_content, core_id=11,  # core_id = 11 is MDC at TOR
                                       number_header_key=vlan_number_header_name,
                                       name_header_key=vlan_name_header_name)
    return vlans


def load_vlan_by_core_id(core_id: int, db_connection: pymysql.Connection):
    cursor = db_connection.cursor()

    # core_id 11 is MDC core from GaaS v1 DB
    query = r'SELECT number, name, core_id, uuid FROM vlans WHERE core_id=%s'
    values = core_id
    cursor.execute(query, values)
    db_data = cursor.fetchall()
    cursor.close()

    vlans = convert_db_data_to_vlans(db_data=db_data)

    return vlans


def insert_vlan(vlan: Vlan, db_connection: pymysql.Connection):
    """Insert the vlan into the gaas v1 DB"""
    import uuid

    cursor = db_connection.cursor()
    query = r'INSERT INTO vlans (core_id, number, name, description, state_id, uuid) VALUES (%s,%s,%s,%s,%s,%s)'
    # core_id 11 is MDC core from GaaS v1 DB, state 2 is deployed
    values = (vlan.core, vlan.number, vlan.name, vlan.description, 2, uuid.uuid4().__str__())
    try:
        cursor.execute(query, values)
        db_connection.commit()
        logging.info('vlan #%s was created' % vlan.number)
    except pymysql.IntegrityError:
        logging.error('vlan #%s was found duplicate' % vlan.number)


def update_vlan(file_vlan: Vlan, db_vlan: Vlan, db_connection: pymysql.Connection):
    """Update the vlan"""
    cursor = db_connection.cursor()
    query = r'UPDATE vlans SET name=%s, description=%s WHERE uuid=%s'
    values = (file_vlan.name, file_vlan.description, db_vlan.uuid)
    cursor.execute(query, values)
    db_connection.commit()
    logging.info('vlan #%s was updated' % db_vlan.number)


def is_real_vlan(number, name):
    """Validate that the number and the name received can be a vlan"""
    import re

    valid_number = False
    valid_name = False

    try:
        int(number)
        valid_number = True
    except ValueError:
        pass

    words_in_name = re.findall(r"[\w']+", name.casefold())
    unwanted_words = ['reserved', 'available']
    intersect = list(set(words_in_name) & set(unwanted_words))

    if len(intersect) == 0:
        valid_name = True

    return valid_number and valid_name


def convert_file_data_to_vlans(file_data, core_id, number_header_key='number', name_header_key='name'):
    """Loop over the file data and if data can be a vlan instantiate it"""
    # TODO: change core_id for something that could be provided by the file
    vlans = list()
    for row in file_data:
        number, name = row[number_header_key], row[name_header_key]

        if is_real_vlan(number, name):
            vlan = Vlan(number=number, name=name, core=core_id)
            vlans.append(vlan)

    return vlans


def convert_db_data_to_vlans(db_data):
    """Loop over db vlan array and instantiate it as Vlan"""
    vlans = list()
    for number, name, core_id, uuid in db_data:
        vlan = Vlan(number=number, name=name, core=core_id, uuid=uuid)
        vlans.append(vlan)

    return vlans


if __name__ == "__main__":
    pass
