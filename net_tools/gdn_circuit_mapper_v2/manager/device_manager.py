from typing import Union

from net_tools.gdn_circuit_mapper_v2.classes.device import Device
from net_tools.gdn_circuit_mapper_v2.commands.device_bd_parser_cmd import ParseNewGDNBridgeDomainConfigCommand
from net_tools.gdn_circuit_mapper_v2.commands.device_int_parser_cmd import ParseNewGDNInterfaceConfigCommand
from net_tools.gdn_circuit_mapper_v2.commands.device_parser_cmd import DeviceConfigParser
from net_tools.gdn_circuit_mapper_v2.services.device_net_connector import DeviceNetworkConnector
from net_tools.gdn_circuit_mapper_v2.services.device_repository import DeviceRepository
import logging


class DeviceManager:

    def __init__(self):
        logging.basicConfig(format='%(asctime)-15s %(hostname)-8s %(message)s',
                            filename=r'C:\Users\vincent.corriveau\Documents\Workshop\tool_box\logs\device_manager.log',
                            level=logging.INFO)
        logging.getLogger('device')

        self._device_repo = DeviceRepository()
        self._device_net_connector = DeviceNetworkConnector()

    def save_device(self, device: Device):
        self._device_repo.add_device(device=device)

    def update_device_config(self, device: Device):
        """
        Try to get the device config from the repo first and if repo is empty use the device connector to get it from
        the device and update the repo
        :param device:
        :return:
        """
        device_from_repo = self._device_repo.get_device_by_hostname(hostname=device.hostname)

        if device_from_repo:
            logging.info('Config found in local storage', extra={'hostname': device.hostname})
            device.config = device_from_repo.config
        else:
            logging.warning('Config not found in local storage, initiate device show run command',
                            extra={'hostname': device.hostname})
            cmd_output = self._device_net_connector.run_command_against_device(device=device, cmd='show run')
            device.config = cmd_output
            self.save_device(device)

    def parse_device(self, device: Device, command: Union[ParseNewGDNInterfaceConfigCommand,
                                                          ParseNewGDNBridgeDomainConfigCommand]):
        parser = DeviceConfigParser(command)
        return parser.parse(device)
