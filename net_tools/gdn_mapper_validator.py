from common.json_tool import load_file


def validate_OTT_neighbor(neighbor_ips) -> bool:
    ott_possible_neighbor_int = ['10.206.232.33', '10.206.232.3', '10.206.254.5', '10.206.232.129', '10.206.232.65',
                                 '10.206.232.32', '10.206.232.2', '10.206.232.128', '10.206.232.64', '10.206.254.6']

    ott_neighbors = set(ott_possible_neighbor_int)
    device_neighbors = set(neighbor_ips)

    # compare the two list and if their intersection is greater then 0 it means that at least one nei
    return len(ott_neighbors.intersection(device_neighbors)) > 0


def validate_endpoint_discovery(map: dict) -> bool:
    endpoints_count = len(map)

    return endpoints_count >= 4 and endpoints_count % 2 == 0


def validate_vpn_id(vpn_id, vfi_name, bd_name) -> bool:
    """Validate if VPN-ID match their bridge domain name and vfi-name"""
    vpn_id_in_vfi_name = vpn_id in vfi_name
    vpn_id_in_bd_name = vpn_id in bd_name

    return vpn_id_in_vfi_name and vpn_id_in_bd_name


def validate_map(gdn_map: dict) -> dict:
    """Validate that the map has no anomalies and return them if found"""
    for vpn_id in gdn_map:

        vpn_endpoints = gdn_map.get(vpn_id).items()
        neighbor_ip_list = []

        for device_name, values in vpn_endpoints:
            for key, values in values.items():
                if key == 'bridge-domains':
                    for element in values:
                        for inner_key, inner_values in element.items():
                            valid = validate_vpn_id(vpn_id=vpn_id,
                                                    vfi_name=inner_values.get('vfi-name'),
                                                    bd_name=inner_key)
                            if not valid:
                                print('Found VPN-ID anomalies in:%s DB:%s VPN-ID:%s' % (device_name, inner_key, vpn_id))

                            # extract neighbors IPs from the sub keys
                            neighbor_ip_list = [neighbors.get('ip') for neighbors in inner_values.get('neighbors')]

        valid = validate_endpoint_discovery(vpn_endpoints)

        if not valid:
            print('Found ENDPOINTS anomalies in:%s only %s device(s) discovered' % (vpn_id, len(vpn_endpoints)))

            if validate_OTT_neighbor(neighbor_ip_list):
                print('anomalies could be related OTTAWA devices not being mapped. Manual validation required')

    return dict()


def main():
    """Entry point"""
    # file_location = input('Enter your json file path : ')
    file_location = r'C:\Users\vincent.corriveau\Documents\Workshop\tool_box\_file_output\gdn_circuit_map.json'
    file_data = load_file(file_location=file_location)
    anomalies = validate_map(file_data)


if __name__ == "__main__":
    import doctest

    doctest.testmod(main())
