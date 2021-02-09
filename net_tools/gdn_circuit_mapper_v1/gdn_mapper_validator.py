from common.json_tool import load_file, output_to_json_file

xstr = lambda s: s or ""


def validate_odc_neighbor(neighbor_ips) -> bool:
    ott_possible_neighbor_int = ['10.206.232.33', '10.206.232.3', '10.206.254.5', '10.206.232.129', '10.206.232.65',
                                 '10.206.232.32', '10.206.232.2', '10.206.232.128', '10.206.232.64', '10.206.254.6']

    ott_neighbors = set(ott_possible_neighbor_int)
    device_neighbors = set(neighbor_ips)

    # compare the two list and if their intersection is greater then 0 it means that at least one nei
    return len(ott_neighbors.intersection(device_neighbors)) > 0


def validate_endpoint_discovery(map: dict) -> bool:
    endpoints_count = len(map)

    return endpoints_count >= 4 and endpoints_count % 2 == 0


def validate_endpoint_symmetry(map: dict) -> bool:
    from collections import Counter

    endpoints = map
    crop_endpoint_names = []
    counter_valid = []

    for device, values in endpoints:
        crop_endpoint_names.append(device.split('1R')[0])

    # loop over each counter result and device must be present 2 time to show his symmetrical
    for key, counter in Counter(crop_endpoint_names).items():
        counter_valid.append(counter == 2)

    return all(counter_valid)


def validate_vpn_id(vpn_id, vfi_name, bd_name) -> bool:
    """Validate if VPN-ID match their bridge domain name and vfi-name"""
    vpn_id_in_vfi_name = vpn_id in vfi_name
    vpn_id_in_bd_name = vpn_id in bd_name

    return vpn_id_in_vfi_name and vpn_id_in_bd_name


def validate_map(gdn_map: dict) -> dict:
    """Validate that the map has no anomalies and return them if found"""
    config_slice = {}

    for vpn_id in gdn_map:
        vpn_endpoints = gdn_map.get(vpn_id).items()
        neighbor_ip_list = []
        bd_error = None
        device_count_error = None
        possible_odc_warning = None
        sym_error = None

        for device_name, values in vpn_endpoints:
            for key, values in values.items():
                if key == 'bridge-domains':
                    for element in values:
                        for inner_key, inner_values in element.items():
                            valid = validate_vpn_id(vpn_id=vpn_id,
                                                    vfi_name=inner_values.get('vfi-name'),
                                                    bd_name=inner_key)
                            if not valid:
                                bd_error = 'hostname:%s DB:%s vpn:%s don\'t match' % (device_name, inner_key, vpn_id)

                            # extract neighbors IPs from the sub keys
                            neighbor_ip_list = [neighbors.get('ip') for neighbors in inner_values.get('neighbors')]

        valid = validate_endpoint_discovery(vpn_endpoints)

        if not valid:
            device_count_error = 'only %s device(s) discovered' % len(vpn_endpoints)

            if validate_odc_neighbor(neighbor_ip_list):
                possible_odc_warning = 'but could be related to ODC. Manual validation required'

        valid = validate_endpoint_symmetry(vpn_endpoints)
        if not valid:
            sym_error = 'possible symmetrical config'

        if bd_error or device_count_error or possible_odc_warning or sym_error:
            print('Found anomalies in VPN-ID:', vpn_id,
                  xstr(bd_error),
                  xstr(device_count_error),
                  xstr(sym_error),
                  xstr(possible_odc_warning))

            config_slice.update({vpn_id: gdn_map.get(vpn_id)})

    return config_slice


def main():
    """Entry point"""
    # file_location = input('Enter your json file path : ')
    file_location = r'C:\Users\vincent.corriveau\Documents\Workshop\tool_box\_file_output\gdn_circuit_map_2021-02-09-14-30-47.json'
    file_data = load_file(file_location=file_location)
    anomalies = validate_map(file_data)
    output_to_json_file(file_name='gdn_mapper_validation', dict_data=anomalies)


if __name__ == "__main__":
    import doctest

    doctest.testmod(main())
