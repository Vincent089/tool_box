class NetInterfaceIterator:
    def __init__(self, list, start, stop):
        self._list = list
        self._start = start
        self._stop = stop

    def __iter__(self):
        return self

    def __next__(self):
        if self._start > self._stop or self._start > len(self._list):
            raise StopIteration

        current = self._start
        self._start += 1

        return self._list[current - 1]
