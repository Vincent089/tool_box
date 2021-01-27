import getpass
from ciscoconfparse import CiscoConfParse
from common.user import User
from net_tools import Device
from net_tools import DeviceBuilder
from net_tools import DeviceCommand
from net_tools import DeviceConfigExporter
from net_tools import DeviceConnector
from net_tools import NetInterface


class ConfigDeviceBuilder(DeviceBuilder):

    def __init__(self, ip, os):
        self._device_mgmnt_ip = ip
        self._device_os = os

    def build_device(self):
        # prompt for a username
        print('\nYou username is needed to collect any device configuration if need be')
        username = input('Enter username (default = %s) :' % getpass.getuser())

        # setup the user to be use for every device connection during script run
        user = User(username=username) if username != '' else User()
        user.ask_password()

        # initiate a connection with the device and retrieve it running configuration
        device_connection = DeviceConnector(ip=self._device_mgmnt_ip,
                                            os=self._device_os,
                                            user=user)
        command = DeviceCommand(device_connection, 'show run')
        device_config = command.run_command()

        self._device = Device(hostname='builded_device',
                              ip=self._device_mgmnt_ip,
                              os=self._device_os,
                              config=device_config)

    def build_interface(self):
        if self._device.config:

            config_exporter = DeviceConfigExporter(self._device.config, 'interface')

            parse = CiscoConfParse(self._device.config.splitlines())

            # Return a list of all interfaces
            interface_cmds = parse.find_objects('^interface')

            # iterate over the resulting IOSCfgLine objects
            for interface_cmd in interface_cmds:
                # get the interface name (remove the interface command from the configuration line)
                interface_name = interface_cmd.text[len('interface\s'):]

                interface_desc = 'not set'
                for cmd in interface_cmd.re_search_children(r'^\sdescription\s'):
                    interface_desc = cmd.text.strip()[len('description\s'):]

                interface_encap = 'not set'
                for cmd in interface_cmd.re_search_children(r'^\sencapsulation\s'):
                    interface_encap = cmd.text.strip()[len('encapsulation\s'):]

                interface_rewrite = 'not set'
                for cmd in interface_cmd.re_search_children(r'^\srewrite\s'):
                    interface_rewrite = cmd.text.strip()[len('rewrite\s'):]

                interface_serv_policies = {'input': 'not set', 'output': 'not set'}
                for cmd in interface_cmd.re_search_children(r'^\sservice-policy\sinput\s'):
                    interface_serv_policies['input'] = cmd.text.strip()[len('service-policy\sinput\s'):]

                # output command
                for cmd in interface_cmd.re_search_children(r'^\sservice-policy\soutput\s'):
                    interface_serv_policies['output'] = cmd.text.strip()[len('service-policy output\s'):]

                self._device.connect(NetInterface(name=interface_name))

    def build_bridge_group(self):
        pass

    def get_device(self) -> Device:
        return self._device
