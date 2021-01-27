import getpass
import json

from common.date_tool import timestamp, timestamp_to_string
from common.db_tool import create_connection

# Notes!
# Log to a device and list the Loopback interfaces
# show ip int brief | include oo

# list of gdn device related to GDN
from common.user import User
from net_tools.classes.device import Device
from net_tools.classes.device_command import DeviceCommand
from net_tools.classes.device_connector import DeviceConnector

deviceList = (
    # mtl
    ('CAMTLCDJ1R100', {'ip': '10.206.254.2', 'os': 'cisco_ios'}),
    ('CAMTLDIC1R100', {'ip': '10.206.254.1', 'os': 'cisco_ios'}),
    ('CAMTLDIC1R500', {'ip': '10.206.254.3', 'os': 'cisco_xr'}),
    ('CAMTLDIC1R600', {'ip': '10.206.254.4', 'os': 'cisco_xr'}),
    ('CAMTLVSL1R500', {'ip': '10.206.254.26', 'os': 'cisco_xr'}),
    ('CAMTLVSL1R600', {'ip': '10.206.254.27', 'os': 'cisco_xr'}),
    # mdc
    ('CATORMDC1R100', {'ip': '10.206.254.7', 'os': 'cisco_ios'}),
    ('CATORMDC1R200', {'ip': '10.206.254.8', 'os': 'cisco_ios'}),
    ('CATORMDC1R500', {'ip': '10.206.254.10', 'os': 'cisco_xr'}),
    ('CATORMDC1R600', {'ip': '10.206.254.9', 'os': 'cisco_xr'}),
    # sdc
    ('CASAGSDC1R300', {'ip': '10.206.254.21', 'os': 'cisco_xr'}),
    ('CASAGSDC1R400', {'ip': '10.206.254.22', 'os': 'cisco_xr'}),
    # rdc
    ('CAREGDC1R300', {'ip': '10.206.254.19', 'os': 'cisco_xr'}),
    ('CAREGDC1R400', {'ip': '10.206.254.20', 'os': 'cisco_xr'}),
    # odc
    ('CAOTTBLA1R100', {'ip': '10.206.254.5', 'os': 'cisco_ios'}),
    ('CAOTTBLA1R200', {'ip': '10.206.254.6', 'os': 'cisco_ios'}),
    # pdc
    ('USPHXSOU1R100', {'ip': '10.206.254.17', 'os': 'cisco_ios'}),
    ('USPHXSOU1R200', {'ip': '10.206.254.18', 'os': 'cisco_ios'}),
)


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


# Entry point
if __name__ == "__main__":
    # access to local device config storage
    devices = create_device_config_model()

    # prompt for a username
    print('\nYou username is needed to collect any device configuration if need be')
    username = input('Enter username (default = %s) :' % getpass.getuser())

    # setup the user to be use for every device connection during script run
    user = User(username=username) if username != '' else User()
    user.ask_password()

    results = {}

    for host_key, host_detail in deviceList:
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

    file_name = 'gdn_circuit_map_%s.json' % timestamp_to_string()
    with open('../_file_output/%s' % file_name, 'w') as file:
        file.write(json.dumps(results))

    print('\nMap completed\nSee file \'%s\'' % file_name)
