from net_tools.config_parser.classes.device import Device
from net_tools.config_parser.commands.device_bridge_domain_cmd import DeviceBridgeDomainCommand
from net_tools.config_parser.commands.device_full_config_cmd import DeviceFullConfigurationCommand
from net_tools.config_parser.lists import gdn_devices
from net_tools.config_parser.manager.device_manager import DeviceManager


def output_device_to_file(device: Device):
    from config import output_location
    file = open('%s/%s_config' % (output_location, device.hostname), 'w')
    file.write(device.config)
    file.close()


def load_config(devices: [Device]):
    """Load device's configuration"""
    for device in devices:
        manager.update_device_config(device)


def read_config(device: Device):
    config = manager.parse_device(device=device, command=DeviceFullConfigurationCommand)

    for obj in config:
        print(obj)


def read_bridge_domains(device: Device):
    """Not working..."""
    config = manager.parse_device(device=device, command=DeviceBridgeDomainCommand)

    config_slice = [obj for obj in config if '3017' in obj.text]
    result = [config.find_all_children(obj.text) for obj in config_slice]

    print('\n'.join(result))


def main():
    load_config(devices=gdn_devices)

    device = [device for device in gdn_devices if device.hostname == 'CATORMDC1R500'].pop()

    output_device_to_file(device=device)


if __name__ == "__main__":
    import doctest

    manager = DeviceManager()
    gdn_devices = gdn_devices.gdn_device_list
    doctest.testmod(main())
