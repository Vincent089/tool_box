from ciscoconfparse import CiscoConfParse

from net_tools.config_parser.classes.device import Device


class DeviceCommand:

    def __init__(self, device: Device):
        self._parsed_config = CiscoConfParse(device.config.splitlines())

    def execute(self):
        raise NotImplemented
