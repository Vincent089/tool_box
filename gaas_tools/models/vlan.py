class Vlan:
    """Simple vlan class"""

    def __init__(self, number: str, name: str, core: int = None, uuid: str = None):
        self.number = int(number)
        self.name = name[:32].strip().replace(' ', '_').lower() if name != '' else 'VLAN%s' % number.zfill(4)
        self.description = name.strip() if name != '' else None
        self.core = core
        self.uuid = uuid

    def __hash__(self):
        """Telling Magic python how Vlan should be hashed"""
        return hash(self.number)

    def __eq__(self, other):
        """Telling Magic python how Vlan are equal"""
        if isinstance(other, Vlan):
            return self.number == other.number
