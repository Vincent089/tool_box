import logging

from net_tools.config_parser.classes.device import Device
from net_tools.config_parser.services.device_net_connector import DeviceNetworkConnector
from net_tools.config_parser.services.device_repository import DeviceRepository


class DeviceManager:

    def __init__(self):
        logging.basicConfig(filename=r'C:\Users\vincent.corriveau\Documents\Workshop\tool_box\logs\device_manager.log',
                            level=logging.INFO)
        logging.getLogger('device')

        self._device_repo = DeviceRepository()
        self._device_net_connector = DeviceNetworkConnector()

    def save_device(self, device: Device):
        """Add a device to the local repo"""
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

    def parse_device(self, device: Device, command):
        """
        Run the received command on the received device
        :param device: Device
        :param command: DeviceCommand
        :return:
        """
        parser_cmd = command(device)
        return parser_cmd.execute()
