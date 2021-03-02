import logging

import pymysql

from gaas_tools.services import vlan_services


def main():
    file_vlans = vlan_services.load_vlan_from_file(file_path=file_path, delimiter='\t')
    db_vlans = vlan_services.load_vlan_by_core_id(core_id=11, db_connection=db)

    vlan_inserted = 0
    vlan_updated = 0

    for file_vlan in file_vlans:
        db_vlan = [vlan for vlan in db_vlans if vlan == file_vlan]

        try:
            db_vlan = db_vlan.pop()

            if file_vlan.name != db_vlan.name:
                logging.warning('%s name don\'t match with the configured name. GaaS Name = %s - Config. Name = %s' %
                                (file_vlan.number, db_vlan.name, file_vlan.name))
                vlan_updated += 1
        except IndexError:
            # Catch pop errors meaning that file vlan wasn't found in db vlans
            logging.error('%s is not found in GaaS DB' % file_vlan.number)
            vlan_inserted += 1

    print('%d vlan updated\n%d vlan created' % (vlan_updated, vlan_inserted))


if __name__ == "__main__":
    import doctest

    db = pymysql.connect('142.101.252.20', 'gaasDev', '!1234567890', 'gaas')
    file_path = r'C:\Users\vincent.corriveau\Documents\Gaas\mdc_vlan_20210222.txt'

    # log stuff
    logging.basicConfig(format='%(levelname)s:%(asctime)-15s:%(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        filename=r'../logs/validate_gaas_v1_vlans.log',
                        level=logging.DEBUG)
    logging.getLogger('vlan_validator')

    doctest.testmod(main())
