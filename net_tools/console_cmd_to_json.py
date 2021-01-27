import json

from common.user import User
from net_tools.classes.device import Device
from net_tools.classes.device_connector import DeviceConnector
from net_tools.classes.device_command import DeviceCommand

deviceList = (
    # mtl
    ('CAMTLCDJ1R100', {'ip': '10.206.254.2', 'os': 'cisco_ios'}),
    # ('CAMTLDIC1R100', {'ip': '10.206.254.1', 'os': 'cisco_ios'}),
    # ('CAMTLDIC1R500', {'ip': '10.206.254.3', 'os': 'cisco_xr'}),
    # ('CAMTLDIC1R600', {'ip': '10.206.254.4', 'os': 'cisco_xr'}),
    # ('CAMTLVSL1R500', {'ip': '10.206.254.26', 'os': 'cisco_xr'}),
    # ('CAMTLVSL1R600', {'ip': '10.206.254.27', 'os': 'cisco_xr'}),
    # # mdc
    # ('CATORMDC1R100', {'ip': '10.206.254.7', 'os': 'cisco_ios'}),
    # ('CATORMDC1R200', {'ip': '10.206.254.8', 'os': 'cisco_ios'}),
    # ('CATORMDC1R500', {'ip': '10.206.254.10', 'os': 'cisco_xr'}),
    # ('CATORMDC1R600', {'ip': '10.206.254.9', 'os': 'cisco_xr'}),
    # # sdc
    # ('CASAGSDC1R300', {'ip': '10.206.254.21', 'os': 'cisco_xr'}),
    # ('CASAGSDC1R400', {'ip': '10.206.254.22', 'os': 'cisco_xr'}),
    # # rdc
    # ('CAREGDC1R300', {'ip': '10.206.254.19', 'os': 'cisco_xr'}),
    # ('CAREGDC1R400', {'ip': '10.206.254.20', 'os': 'cisco_xr'}),
    # # odc
    # ('CAOTTDC1R100', {'ip': '10.206.254.5', 'os': 'cisco_ios'}),
    # ('CAOTTDC1R200', {'ip': '10.206.254.6', 'os': 'cisco_ios'}),
    # # pdc
    # ('USPHXSOU1R100', {'ip': '10.206.254.17', 'os': 'cisco_ios'}),
    # ('USPHXSOU1R200', {'ip': '10.206.254.18', 'os': 'cisco_ios'}),
)


def run_cmd(cmd, device):
    # connection to device and run the received command
    device_connection = DeviceConnector(device, user)
    command = DeviceCommand(device_connection, cmd)
    output = command.run_command()

    return output
    # return json.dumps(output)


# Entry point
if __name__ == "__main__":
    print('Script started')

    # setup user for a device connections
    user = User()
    user._password = 'Pr1est2020!'
    # print('Password for %s is needed to connect on devices' % user.get_user())
    # user.ask_password()

    for host_key, host_detail in deviceList:
        device = Device(hostname=host_key,
                        ip=host_detail.get('ip'),
                        os=host_detail.get('os'))

        result = run_cmd('show vlan', device)

        # write the JSON to the HTML template
        # with open(r'../_file_output/cmd_output.txt', 'w') as f:
        #     f.write(result)

        print(result)

    print('Script ended')
