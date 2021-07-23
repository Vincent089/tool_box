import requests

from common.json_tool import load_file


def get_gaas_auth():
    print('Authenticating to GaaS')
    url = "http://localhost:8000/api-token-auth/"
    payload = dict(username='vincent.corriveau', password='AbiBert1618!')
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


def fetch_circuits_map():
    file_location = r'C:\Users\vincent.corriveau\Documents\Workshop\tool_box\_file_output\gdn_circuit_map_2021-02-09-14-30-47.json'
    file_data = load_file(file_location=file_location)
    return file_data


def main():
    circuits = fetch_circuits_from_gaas()
    map = fetch_circuits_map()

    vpn_numbers = [int(vpn) for vpn in map if vpn != 'not set']
    imported_vpn_number = []

    for circuit in circuits:
        for sub in circuit['sub_circuits']:
            if int(sub['number']) in vpn_numbers:
                imported_vpn_number.append(sub['number'])

    result = set(vpn_numbers).difference(imported_vpn_number)

    for row in result:
        print(row)

    print('\n%s not imported' % len(imported_vpn_number))
    print('%s discovered' % len(map))


if __name__ == "__main__":
    import doctest

    TOKEN = get_gaas_auth()

    doctest.testmod(main())
