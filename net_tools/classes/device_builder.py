from abc import ABC, abstractmethod

from net_tools import Device


class DeviceBuilder(ABC):
    _device: Device

    @abstractmethod
    def build_device(self):
        pass

    @abstractmethod
    def build_interface(self):
        pass

    @abstractmethod
    def build_bridge_group(self):
        pass

    @abstractmethod
    def get_device(self) -> Device:
        return self._device
