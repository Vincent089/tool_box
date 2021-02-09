import pymysql
import csv
from datetime import datetime


def fetch_from_db():
    """
    Fetch data needed for Brian Project from the old GaaS v1 database
    Field fetched are based on Jean and Etienne request
    :return:
    """
    db = pymysql.connect('142.101.252.20', 'gaasDev', '!1234567890', 'gaas')
    db_data = None

    if db is not None:
        cursor = db.cursor()
        query = """select d.name,
       l.prefix       location,
       d2.name        datacenter,
       c.name         core,
       ev.hardware as model,
       ei.port,
       ei.description,
       ei.admin_status,
       ei.status
from equipments d
         inner join datacenters d2 on d.datacenter_id = d2.id
         left join cores c on d.core_id = c.id
         left join locations l on d.location_id = l.id
         left join (
    select ev.equipment_id,
           ev.hardware
    from equipment_version ev
    where DATE(ev.createdate) = DATE(NOW())
) ev on d.id = ev.equipment_id
         left join (
    select ei.equipment_id,
           ei.port,
           ei.description,
           ei.admin_status,
           ei.status
    from equipment_interface ei
    where DATE(ei.createdate) = DATE(NOW())
) ei on d.id = ei.equipment_id
where d.datacenter_id in (1, 3, 5, 7) # Montreal, Saguenay, Toronto, Regina
order by d.name"""

        cursor.execute(query)
        db_data = cursor.fetchall()

    db.close()

    return db_data


def fetch_from_csv():
    # user entry
    # file_location = input('Enter the csv file path : ')
    file_location = r'C:\Users\vincent.corriveau\Documents\Workshop\tool_box\_file_output\brian_data_2020-10-02-14-10-29.csv'

    # read data csv and format various object to be use uin Graph
    with open(file_location, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        result = list(csv_reader)

    return result


def save_data_to_csv(data_to_save):
    """
    Save a dict to a csv object and save it on disk
    :param data_to_save:
    :return:
    """
    doc_name = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    with open('../_file_output/brian_data_' + str(doc_name) + '.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile,
                                fieldnames=['name', 'location', 'datacenter', 'core', 'model', 'port', 'description',
                                            'admin_status', 'status'],
                                delimiter=';')
        writer.writeheader()
        writer.writerows(data_to_save)


def convert_tuple_to_dict(db_tuple):
    raw_data = []
    for (name, location, datacenter, core, model, port, description, admin_status, status) in db_tuple:
        if name not in excluded_device_name:
            # convert the tuple data into a dict
            raw_data.append({
                'name': name,
                'location': location,
                'datacenter': datacenter,
                'core': core,
                'model': model,
                'port': port,
                'description': description,
                'admin_status': admin_status,
                'status': status
            })

    return raw_data


# Entry point
if __name__ == "__main__":
    # List of excluded device
    excluded_device_name = ('gdn_circuit_mapper_v2', 'phoenix', 'bell', 'montrea', 'regina', 'saguenay', 'ottawa', 'montreal', 'client',
                            'fcc - core', 'remote', 'fcc-dc', 'curvature', 'testgdnrouter2', 'testgdnrouter1',
                            'testgdnrouter3', 'testgdnrouter4')

    # from work speed fetch db data them save it to local csv, then work on it. Do so comment/uncomment the right line
    # data_list = fetch_from_db()
    # data = convert_tuple_to_dict(data_list)
    # save_data_to_csv(data_to_save=data)

    data = fetch_from_csv()

    result = {}
    for item in data:
        if item['name'] not in result.keys() and item['name'] not in excluded_device_name:
            result[item['name']] = {
                'model': item['model'],
                'location': item['location'],
                'datacenter': item['datacenter'],
                'core': item['core'],
                'port_up': 0,
                'port_total': 0,
                'fex_count': 0,
                'fex_detail': []
            }

        if item['port'] is not '':

            # Count and asset active ports
            if item['admin_status'] == 'up' or item['status'] == 'connected':
                result[item['name']]['port_up'] += 1

            result[item['name']]['port_total'] += 1

            # Count and asset FEX ports
            if 'fex' in item['description'].lower():
                result[item['name']]['fex_count'] += 1
                result[item['name']]['fex_detail'].append(item['port'])

    # convert result back to csv
    csv_formatted_array = []
    for key, value in result.items():
        # console output purpose
        print(key, value)

        formatted_dict = {'name': key}  # start with x's keys and values
        formatted_dict.update(value)
        csv_formatted_array.append(formatted_dict)

    current_datetime = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    with open('../_file_output/brian_data_' + str(current_datetime) + '_format.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile,
                                fieldnames=['name', 'location', 'datacenter', 'core', 'model', 'port_up', 'port_total',
                                            'fex_count', 'fex_detail'],
                                delimiter=';')
        writer.writeheader()
        writer.writerows(csv_formatted_array)
