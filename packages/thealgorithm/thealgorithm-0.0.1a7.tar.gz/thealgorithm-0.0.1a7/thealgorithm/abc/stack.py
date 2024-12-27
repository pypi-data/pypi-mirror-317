class Stack:
    def __init__(self, max_size: int):
        self._max_size = max_size
        self._size = 0
        self._items = []

    def push(self, object) -> bool:
        if self.size < self._max_size:
            self._items.append(object)
            self._size += 1
            return True
        return False

    def pop(self):
        if self.is_empty():
            return None
        self._size -= 1
        return self._items.pop()

    def top(self):
        if self.size == 0:
            return None
        return self._items[-1]

    def is_empty(self):
        return self._size == 0

    @property
    def size(self):
        return self._size
