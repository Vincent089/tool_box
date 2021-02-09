from net_tools.config_parser.classes.device import Device
from net_tools.config_parser.commands.device_cmd import DeviceCommand


class DeviceFullConfigurationCommand(DeviceCommand):
    def __init__(self, device: Device):
        super(DeviceFullConfigurationCommand, self).__init__(device=device)

    def execute(self):
        return self._parsed_config.objs
