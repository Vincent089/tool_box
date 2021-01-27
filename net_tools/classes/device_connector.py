from netmiko import ConnectHandler
from netmiko.ssh_exception import AuthenticationException
from netmiko.ssh_exception import NetMikoTimeoutException


class DeviceConnector:
    _connection = None

    def __init__(self, device, user):
        '''
        Initialize a class to interact between device and user object
        :param device: Device
        :param user: DeviceUser
        '''
        self._device = device
        self._user = user

    def execute(self, command):
        '''
        Establish a connection to the device and execute the received command
        :param command:
        :return:
        '''
        result = None
        self.connect_to_device()
        if self._connection is not None:
            result = self._connection.send_command(command)
            self.disconnect_from_device()

        return result

    def disconnect_from_device(self):
        '''
        If connection exist, disconnect
        :return:
        '''
        if self._connection:
            self._connection.disconnect()

    def connect_to_device(self):
        '''
        Establish connection to the device and store it
        :return:
        '''
        self._connection = self._connection_initializer()

    def test_connection(self):
        '''
        Validate if user and device maintain a connection
        :return:
        '''
        self.connect_to_device()

        # Print message if connection is OK
        if self._connection.is_alive():
            print('Connection to %s worked' % self._device.hostname)

        self.disconnect_from_device()

    def _connection_initializer(self):
        '''
        Tries to initiate a SSH connection to the device and return the connection object
        :return:
        '''
        try:
            print('Connecting to : %s ...' % self._device.ip)
            net_connect = ConnectHandler(ip=self._device.ip,
                                         device_type=self._device.os,
                                         username=self._user.get_user(),
                                         password=self._user.get_pwd())

        except NetMikoTimeoutException:
            return print('\tConnection timed out')
        except AuthenticationException:
            return print('\tAuthentication failure')

        return net_connect
