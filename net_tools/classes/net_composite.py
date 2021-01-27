from net_tools import NetElement
from typing import List


class NetComposite(NetElement):
    def __init__(self, name):
        self.name = name
        self.net_elements: List[NetElement] = []

    def connect(self, net_element: NetElement):
        self.net_elements.append(net_element)
        net_element.parent = self

    def disconnect(self, net_element: NetElement):
        self.net_elements.remove(net_element)
        net_element.parent = None

    def get_structure(self):
        return {self: [item.get_structure() for item in self.net_elements]}
