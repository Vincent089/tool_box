import logging

import pymysql
from pymysql import IntegrityError

from .models.vlan import Vlan


def load_mdc_vlan_from_csv():
    from common.csv_tool import load_file_with_header
    file_path = r'C:\Users\vincent.corriveau\Documents\Gaas\mdc_vlan_20210219.csv'
    return load_file_with_header(file_path=file_path)


def load_mdc_vlan_from_db():
    cursor = db.cursor()

    # core_id 11 is MDC core from GaaS v1 DB
    query = r'SELECT number, name, uuid FROM vlans WHERE core_id=11'
    cursor.execute(query)
    db_data = cursor.fetchall()
    cursor.close()

    return db_data


def insert_vlan(vlan: Vlan):
    """Insert the vlan into the gaas v1 DB"""
    import uuid

    cursor = db.cursor()
    query = r'INSERT INTO vlans (core_id, number, name, description, state_id, uuid) VALUES (%s,%s,%s,%s,%s,%s)'
    # core_id 11 is MDC core from GaaS v1 DB, state 2 is deployed
    values = (11, vlan.number, vlan.name, vlan.description, 2, uuid.uuid4().__str__())
    try:
        cursor.execute(query, values)
        db.commit()
        logging.info('vlan #%s was created' % vlan.number)
    except IntegrityError:
        logging.error('vlan #%s was found duplicate' % vlan.number)


def update_vlan(file_vlan: Vlan, db_vlan: Vlan):
    """Update the vlan"""
    cursor = db.cursor()
    query = r'UPDATE vlans SET name=%s, description=%s WHERE uuid=%s'
    values = (file_vlan.name, file_vlan.description, db_vlan.uuid)
    cursor.execute(query, values)
    db.commit()
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


def convert_file_date_to_vlans(file_data):
    """Loop over the file data and if data can be a vlan instantiate it"""
    vlans = list()
    for row in file_data:
        number, name = row['VLAN'], row['Name']

        if is_real_vlan(number, name):
            vlan = Vlan(number=number, name=name)
            vlans.append(vlan)

    return vlans


def convert_db_data_to_vlans(db_data):
    """Loop over db vlan array and instantiate it as Vlan"""
    vlans = list()
    for number, name, uuid in db_data:
        vlan = Vlan(number=number, name=name, uuid=uuid)
        vlans.append(vlan)

    return vlans


def main():
    file_content = load_mdc_vlan_from_csv()
    db_content = load_mdc_vlan_from_db()
    file_vlans = convert_file_date_to_vlans(file_content)
    db_vlans = convert_db_data_to_vlans(db_content)

    vlan_inserted = 0
    vlan_updated = 0

    for file_vlan in file_vlans:
        db_vlan = [vlan for vlan in db_vlans if vlan == file_vlan]

        try:
            db_vlan = db_vlan.pop()
            update_vlan(file_vlan, db_vlan)
            vlan_updated += 1
        except IndexError:
            # Catch pop errors meaning that file vlan wasn't found in db vlans
            insert_vlan(file_vlan)
            vlan_inserted += 1

    print('%d vlan updated\n%d vlan created' % (vlan_updated, vlan_inserted))


if __name__ == "__main__":
    import doctest

    db = pymysql.connect('142.101.252.20', 'gaasDev', '!1234567890', 'gaas')

    logging.basicConfig(format='%(levelname)s:%(asctime)-15s:%(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        filename=r'/logs/import_mdc_vlan_prod_v1.log',
                        level=logging.DEBUG)
    logging.getLogger('vlan_importer')

    doctest.testmod(main())
