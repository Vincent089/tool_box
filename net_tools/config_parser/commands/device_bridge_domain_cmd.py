from net_tools.config_parser.classes.device import Device
from net_tools.config_parser.commands.device_cmd import DeviceCommand


class DeviceBridgeDomainCommand(DeviceCommand):
    def __init__(self, device: Device):
        super(DeviceBridgeDomainCommand, self).__init__(device=device)

    def execute(self):
        """Return a str of all bridge domains"""
        result = []
        bd_list = self._parsed_config.find_objects(r'bridge-domain\s')

        for bd in bd_list:
            print(bd)
            result += self._parsed_config.find_all_children(bd.text)

        return '\n'.join(result)





































