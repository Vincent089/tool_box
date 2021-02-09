from common.csv_tool import build_list_from_csv, build_csv_with_headers
from net_tools.gdn_circuit_mapper_v2.commands.device_bd_parser_cmd import ParseNewGDNBridgeDomainConfigCommand
from net_tools.gdn_circuit_mapper_v2.commands.device_int_parser_cmd import ParseNewGDNInterfaceConfigCommand
from net_tools.gdn_circuit_mapper_v2.manager.device_manager import DeviceManager
from net_tools.gdn_circuit_mapper_v2.lists.gdn_devices import new_gdn_device_list


def load_circuit_csv():
    file_location = r'C:\Users\vincent.corriveau\Documents\Workshop\tool_box\_file_input\gdn_master_circuit_list.csv'
    return build_list_from_csv(file_location=file_location, delimiter=',')


def append_config_slice_result(key, config_slice, result_dict):
    result_dict.update({key: config_slice})


def discover_config_from_new_gdn(circuit_id, vpn_id):
    devices = new_gdn_device_list

    # upload each device config
    for device in devices:
        manager.update_device_config(device)

    config_slices = []
    # parse each device config and run specific command on each of them
    for device in devices:
        config_int_slice = manager.parse_device(device=device,
                                                command=ParseNewGDNInterfaceConfigCommand(
                                                    circuit_id=circuit_id,
                                                    sub_id=vpn_id))

        config_bd_slice = manager.parse_device(device=device,
                                               command=ParseNewGDNBridgeDomainConfigCommand(
                                                   circuit_id=circuit_id,
                                                   sub_id=vpn_id))

        if config_int_slice or config_bd_slice:
            single_device_config_slice = {}

            append_config_slice_result('hostname', device.hostname, single_device_config_slice)

            if config_int_slice:
                append_config_slice_result('interface', config_int_slice, single_device_config_slice)

            if config_bd_slice:
                append_config_slice_result('bridge_domain', config_bd_slice, single_device_config_slice)

            config_slices.append(single_device_config_slice)

    return config_slices


def main():
    circuit_list = load_circuit_csv()

    for circuit_data in circuit_list:
        print('Work in progress\nCurrently at\n', '%d/%d' % (circuit_list.index(circuit_data), len(circuit_list)), end="\r")

        if circuit_data.get('Source') == 'new':
            config_discovered = discover_config_from_new_gdn(circuit_id=circuit_data.get('Circuit ID'),
                                                             vpn_id=circuit_data.get('VPN-VFI'))
            circuit_data['Config Slice'] = config_discovered

    build_csv_with_headers(file_name='gdn_circuit_with_config_slice',
                           file_rows=circuit_list,
                           file_headers=['Circuit ID', 'VPN-VFI', 'Datacenters', 'Path', 'Client', 'Name', 'Speed',
                                         'Source', 'Config Slice'])


def tester():
    load_circuit_csv()


if __name__ == "__main__":
    import doctest

    manager = DeviceManager()

    doctest.testmod(main())
