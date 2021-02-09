from abc import ABC, abstractmethod


class NetElement(ABC):
    name = None
    parent = None

    def __repr__(self):
        return '%s<%s>' % (self.__class__.__name__, self.name)

    @abstractmethod
    def connect(self, net_element) -> None:
        pass

    @abstractmethod
    def disconnect(self, net_element) -> None:
        pass

    @abstractmethod
    def get_structure(self):
        return self
