from _idea_recycle_bin.config_device_builder import ConfigDeviceBuilder
from _idea_recycle_bin.device_creator import DeviceCreator

if __name__ == '__main__':
    device_1 = DeviceCreator(ConfigDeviceBuilder(ip='10.206.254.3', os='cisco_xr')).create_device()

    print(device_1.get_interfaces())
