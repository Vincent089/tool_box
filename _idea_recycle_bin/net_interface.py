from net_tools import NetComposite


class NetInterface(NetComposite):
    def __init__(self, name, *args):
        super().__init__(name=name)
