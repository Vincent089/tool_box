import requests
import xlsxwriter

from common.date_tool import timestamp_to_string, current_text_month, current_text_year
from config import output_location


def get_gaas_auth():
    print('Authenticating to GaaS')
    url = "http://localhost:8000/api-token-auth/"
    payload = dict(username='vincent.corriveau', password='Cyber!2021')
    response = requests.request("POST", url, data=payload)
    return response.json()['token']


def fetch_circuits_from_gaas():
    """Fetch GDN Circuits from GaaS API"""
    print('Fetching circuits data from GaaS')

    # Fetching information with auth token header
    headers = {
        'Authorization': 'Bearer %s' % TOKEN
    }
    url = "http://localhost:8000/api/v1/gdncircuits/?page_size=500"
    response = requests.request("GET", url, headers=headers)
    return response.json()['results']


def fetch_clients_from_gaas():
    """Fetch Clients from GaaS API"""
    print('Fetching clients data from GaaS')

    # Fetching information with auth token header
    headers = {
        'Authorization': 'Bearer %s' % TOKEN
    }
    url = "http://localhost:8000/api/v1/clients/?page_size=500"
    response = requests.request("GET", url, headers=headers)
    return response.json()['results']


def fetch_core_from_gaas():
    """Fetch Cores from GaaS API"""
    print('Fetching cores data from GaaS')

    # Fetching information with auth token header
    headers = {
        'Authorization': 'Bearer %s' % TOKEN
    }
    url = "http://localhost:8000/api/v1/cores/?page_size=500"
    response = requests.request("GET", url, headers=headers)
    return response.json()['results']


def fetch_datacenter_from_gaas():
    """Fetch Datacenter from GaaS API"""
    print('Fetching datacenters data from GaaS')

    # Fetching information with auth token header
    headers = {
        'Authorization': 'Bearer %s' % TOKEN
    }
    url = "http://localhost:8000/api/v1/datacenters/?page_size=500"
    response = requests.request("GET", url, headers=headers)
    return response.json()['results']


def output_data_to_excel(data):
    print('Building Excel File')
    # Some var setup for names and shits
    workbook_name = r'jean_ru_evidence_report_%s' % timestamp_to_string()
    worksheet_name = r'%s %s' % (current_text_month(), current_text_year())
    output_path = r'%s\%s.xlsx' % (output_location, workbook_name)

    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(output_path)
    worksheet = workbook.add_worksheet(worksheet_name)

    # Some styles format
    worksheet.set_column('A:B', 6)
    worksheet.set_column('C:C', 42)
    worksheet.set_column('D:D', 22)
    worksheet.set_column('E:E', 11)
    worksheet.set_column('F:G', 6)
    worksheet.set_column('H:H', 25)
    worksheet.set_column('I:I', 6)
    worksheet.set_column('J:J', 6)
    worksheet.set_column('K:K', 35)
    worksheet.set_column('L:L', 6)
    worksheet.set_column('M:M', 35)
    worksheet.set_column('N:N', 6)
    worksheet.set_column('O:O', 35)

    title_format = workbook.add_format({'bold': True})

    # Write headers
    worksheet.write('A1', 'RU', title_format)
    worksheet.write('B1', 'RU Cost', title_format)
    worksheet.write('C1', 'Client Name', title_format)
    worksheet.write('D1', 'Mandate', title_format)
    worksheet.write('E1', 'Total (Mb/s)', title_format)
    worksheet.write('F1', 'Circuit ID', title_format)
    worksheet.write('G1', 'Speed', title_format)
    worksheet.write('H1', 'Lien', title_format)
    worksheet.write('I1', 'VPN', title_format)
    worksheet.write('J1', 'Vlans', title_format)

    # Start from the first cell. Rows and columns are zero indexed.
    # Ref. A1 is (0, 0)
    row = 1
    col = 0

    # Iterate over the data and write it out row by row
    for record in data:
        record_len = len(record)
        counter = 0

        while counter < record_len:
            worksheet.write(row, col + counter, record[counter])
            counter += 1
        row += 1

    workbook.close()
    print('Output completed see\t%s' % output_path)


def format_to_excel_data(data):
    # example de data
    # {
    # 	'ru': 'ND098',
    # 	'cost': 1.84,
    # 	'client_name': 'Acxsys Corporate Services',
    # 	'mandate': '30000000003948710652',
    # 	'total_mbps': 1000,
    # 	'circuits': [{
    # 		'cid': '3056',
    # 		'speed': 1000,
    # 		'desc': 'Acxsys (GDN Circuit ID:3056)',
    # 		'sub_circuits': [{
    # 			'number': 1111,
    # 			'vlans': [{
    # 				'number': 2845,
    # 				'name': '10.5.55.0/24_Acxsys_GDN'
    # 			}, {
    # 				'number': 2758,
    # 				'name': '10.5.55.0/24_Acxsys_GDN'
    # 			}]
    # 		}],
    # 		'datacenters': 'Montreal-Toronto'
    # 	}]
    # }

    excel_format = []

    for row in data:
        excel_format.append(
            [row['ru'], float(row['cost']), row['client_name'], row['mandate'], row['total_mbps']])

        for circuit in row['circuits']:
            excel_format.append(
                ['', '', '', '', '', int(circuit['cid']), int(circuit['speed']), circuit['datacenters']])

            for sub_circuit in circuit['sub_circuits']:
                sub_detail = ['', '', '', '', '', '', '', '', int(sub_circuit['number'])]

                for vlan in sub_circuit['vlans']:
                    sub_detail += [vlan['number'], vlan['name']]

                excel_format.append(sub_detail)

    return excel_format


def remap_gaas_data(gaas_data):
    mapped_list = list()

    # return only client data with circuits
    clients_with_circuits = [data for data in gaas_data if len(data['circuits']) > 0]

    for client_with_circuits in clients_with_circuits:
        result = dict(ru='ND098',
                      cost=1.84,
                      client_name=client_with_circuits['full_name'],
                      mandate=client_with_circuits['mandate'],
                      total_mbps=sum(circuit['speed'] for circuit in client_with_circuits['circuits']),
                      circuits=[])

        for circuit in client_with_circuits['circuits']:
            child_result = dict(cid=circuit['number'],
                                speed=circuit['speed'],
                                desc=circuit['description'],
                                sub_circuits=[])

            point_dc_names = [point['core']['datacenter']['name'] for point in circuit['points']]
            circuit_point_as_string = '-'.join(point_dc_names)
            child_result.update(datacenters=circuit_point_as_string)

            for sub_circuit in circuit['sub_circuits']:
                child_of_child_result = dict(number=sub_circuit['number'])
                sub_circuit_vlans = [dict(number=vlan['number'], name=vlan['name']) for vlan in sub_circuit['vlans']]
                child_of_child_result.update(vlans=sub_circuit_vlans)

                child_result['sub_circuits'].append(child_of_child_result)

            result['circuits'].append(child_result)

        mapped_list.append(result)

    return mapped_list


def merge_gaas_data(circuit_data, client_data, core_data, datacenter_data):
    # merge datacenter info into core list
    for core in core_data:
        datacenter = next(dc for dc in datacenter_data if core['datacenter'] == dc['id'])
        core['datacenter'] = datacenter

    # merge core infos into circuit list
    for circuit in circuit_data:
        for point in circuit['points']:
            core = next(core for core in core_data if core['id'] == point['core'])
            point['core'] = core

    # add a "circuits" object list to client list
    for client in client_data:
        client_circuits = [circuit for circuit in circuit_data if circuit['client'] == client['id']]
        client['circuits'] = client_circuits

    return client_data


def main():
    circuits = fetch_circuits_from_gaas()
    clients = fetch_clients_from_gaas()
    cores = fetch_core_from_gaas()
    datacenters = fetch_datacenter_from_gaas()
    merged_data = merge_gaas_data(circuit_data=circuits, client_data=clients, core_data=cores,
                                  datacenter_data=datacenters)
    data = remap_gaas_data(gaas_data=merged_data)
    excel_like_data = format_to_excel_data(data=data)
    output_data_to_excel(data=excel_like_data)


def tester():
    pass


if __name__ == "__main__":
    import doctest

    TOKEN = get_gaas_auth()

    doctest.testmod(main())
