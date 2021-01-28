from typing import Union

from ciscoconfparse import CiscoConfParse

from net_tools.gdn.classes.device import Device
from net_tools.gdn.commands.device_int_parser_cmd import ParseNewGDNInterfaceConfigCommand


class DeviceConfigParser:
    def __init__(self, command: Union[ParseNewGDNInterfaceConfigCommand]):
        self._command = command

    def parse(self, device: Device):
        parsed_config = CiscoConfParse(device.config.splitlines())
        return self._command.execute(parsed_config)
