from net_tools import Device
from net_tools import DeviceBuilder


class DeviceCreator:
    def __init__(self, builder: DeviceBuilder):
        self.builder = builder

    def create_device(self) -> Device:
        self.builder.build_device()
        self.builder.build_interface()

        return self.builder.get_device()
