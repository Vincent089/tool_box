import getpass

from common.user import User
from net_tools.classes.device_command import DeviceCommand
from net_tools.classes.device_connector import DeviceConnector
from net_tools.gdn_circuit_mapper_v2.classes.device import Device


class DeviceNetworkConnector:
    def __init__(self):
        # prompt for a username
        print("""\nDevice Connector needs your username to connect to any device
        This will only be prompt once and will be reuse for each device it needs to connect""")
        username = input('Enter username (default = %s) :' % getpass.getuser())

        # setup the user to be use for every device connection during script run
        self._user = User(username=username) if username != '' else User()
        self._user.ask_password()

    def _connect(self, device: Device) -> DeviceConnector:
        return DeviceConnector(device, self._user)

    def run_command_against_device(self, device: Device, cmd: str) -> str:
        conn = self._connect(device)
        command = DeviceCommand(conn, cmd)

        return command.run_command()
