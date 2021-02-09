import getpass
import json

from common.date_tool import timestamp, timestamp_to_string
from common.db_tool import create_connection
from common.json_tool import load_file
from common.user import User
from net_tools.classes.device import Device
from net_tools.classes.device_command import DeviceCommand
from net_tools.classes.device_connector import DeviceConnector
from net_tools.gdn_circuit_mapper_v1.lists import gdn_devices


def connect_to_device_config_db():
    """Create a simple DB called "deviceconfig" using SQLite and SQLAlchemy"""
    db_file = r"C:\Users\vincent.corriveau\Documents\Workshop\tool_box\_db_repo\deviceconfig.db"
    return create_connection(db_file)


def create_device_config_model():
    """Will create a simple deviceconfig model using SQLAlchemy to save device configs for later use"""
    from sqlalchemy import MetaData, Table, Column, String, DateTime

    metadata = MetaData()
    device_configs = Table('deviceconfigs', metadata,
                           Column('hostname', String, primary_key=True),
                           Column('config', String),
                           Column('timestamp', DateTime))
    metadata.create_all(connect_to_device_config_db())

    return device_configs


def add_device_config(name, config):
    """Add a device configuration to the LocalStorage"""
    engine = connect_to_device_config_db()

    with engine.connect() as conn:
        print('Saving %s\'s config into LocalStorage' % name)
        ins = devices.insert().values(hostname=name,
                                      config=config,
                                      timestamp=timestamp())
        conn.execute(ins)


def select_device_config_from_db(device_name):
    """Try to select the configuration based on the received device name"""
    from sqlalchemy import select
    engine = connect_to_device_config_db()

    with engine.connect() as conn:
        select = select([devices]).where(devices.c.hostname == device_name)
        result = conn.execute(select).fetchone()

        if result:
            return result['config']
        else:
            return None


def pull_config_from_device(device: Device):
    """Connect to a device and get the latest configuration"""
    device_connection = DeviceConnector(device, user)
    command = DeviceCommand(device_connection, 'show run')

    return command.run_command()


def update_map_with_manual_data():
    from os import listdir
    from os.path import isfile, join

    odc_manual_map_location = r'C:\Users\vincent.corriveau\Documents\Workshop\tool_box\_file_input\odc_gdn_map'

    files = [f for f in listdir(odc_manual_map_location) if isfile(join(odc_manual_map_location, f))]

    for file_name in files:
        data = load_file(r'%s/%s' % (odc_manual_map_location, file_name))

        for key, value in data.items():
            results[key] = value


def main():
    for host_key, host_detail in device_list:
        device = Device(hostname=host_key,
                        ip=host_detail.get('ip'),
                        os=host_detail.get('os'))

        # Get the config from local storage or pull it from device if not already saved
        local_config = select_device_config_from_db(device.hostname)
        if local_config is not None:
            print('Getting %s\'s Config from LocalStorage' % device.hostname)
            device.config = local_config
        else:
            print('Getting %s\'s Config from Device' % device.hostname)
            config_from_cmd = pull_config_from_device(device)
            add_device_config(device.hostname, config_from_cmd)
            device.config = config_from_cmd

        if device.config is not None:
            # gets the config part needed to build a map of circuits
            device_interfaces = device.get_interfaces().get('interfaces')
            device_policy_maps = device.get_policy_maps().get('policy-maps')
            device_bridge_domains = device.get_bridge_domains().get('bridge-domains')

            print('Reading config')

            for bridge_name, bridge_details in device_bridge_domains.items():
                # add the vpn id as the prime key is not exist
                if bridge_details['vpn-id'] not in results.keys():
                    results[bridge_details['vpn-id']] = {}

                # add the device hostname as the second level
                results[bridge_details['vpn-id']].update({
                    device.hostname: {'bridge-domains': list(),
                                      'interfaces': list(),
                                      'policy-maps': list()}
                })

                results[bridge_details['vpn-id']][device.hostname]['bridge-domains'].append(
                    {bridge_name: bridge_details})

                # get the interface information used for this bridge domain
                for interface_name, interface_details in device_interfaces.items():
                    if bridge_details['interface'] in interface_name:
                        results[bridge_details['vpn-id']][device.hostname]['interfaces'].append(
                            {interface_name: interface_details})

                        # get the policy map used by the interface found
                        for policy_name, policy_details in device_policy_maps.items():

                            # split each policy into a list to be validate again the current policy name
                            input_policy_name_list = interface_details['service-policy']['input'].split(' ')
                            output_policy_name_list = interface_details['service-policy']['output'].split(' ')

                            if policy_name in input_policy_name_list or policy_name in output_policy_name_list:
                                results[bridge_details['vpn-id']][device.hostname]['policy-maps'].append(
                                    {policy_name: policy_details})

    update_map_with_manual_data()

    file_name = 'gdn_circuit_map_%s.json' % timestamp_to_string()
    with open('../_file_output/%s' % file_name, 'w') as file:
        file.write(json.dumps(results))

    print('\nMap completed\nSee file \'%s\'' % file_name)


def tester():
    update_map_with_manual_data()


if __name__ == "__main__":
    import doctest

    # Global Vars
    device_list, devices, results = gdn_devices.device_list, create_device_config_model(), {}

    # prompt for a username
    print('\nYou username is needed to collect any device configuration if need be')
    username = input('Enter username (default = %s) :' % getpass.getuser())

    # setup the user to be use for every device connection during script run
    user = User(username=username) if username != '' else User()
    user.ask_password()

    doctest.testmod(main())
