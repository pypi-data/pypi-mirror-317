from ..sorting import quick


class Iter:
    def __init__(self):
        self._size = 0

    def __len__(self):
        return self._size

    def __bool__(self):
        return len(self) != 0

    def sort(self, reverse=False):
        quick(self, 0, len(self) - 1, reverse)
