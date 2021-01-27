from typing import List
from net_tools import NetBridgeGroup
from net_tools import NetComposite
from net_tools import NetElement

from net_tools import NetInterface


class Device(NetComposite):
    def __init__(self, hostname, ip, os, config=None):
        super().__init__(hostname)
        self.ip = ip
        self.os = os
        self.config = config

    def get_interfaces(self) -> List[NetElement]:
        return [item for item in self.net_elements if item.__class__ == NetInterface]

    def get_bridges(self) -> List[NetElement]:
        return [item for item in self.net_elements if item.__class__ == NetBridgeGroup]
