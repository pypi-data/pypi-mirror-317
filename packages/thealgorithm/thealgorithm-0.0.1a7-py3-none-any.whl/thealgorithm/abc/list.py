from collections.abc import Iterable
from .iter import Iter


class Node:
    def __init__(self, data, next=None, prev=None):
        self.value = data
        self.next = next
        self.prev = next

    def __repr__(self) -> str:
        return f"Node({str(self.value)})"


class LinearList(Iter):
    def __init__(self):
        super().__init__()
        self._head = None

    def __repr__(self):
        _str = "[ "
        curr = self._head
        while curr is not None:
            _str += str(curr.value) + " "
            curr = curr.next
        return _str + "]"

    def __iter__(self):
        self._curr = self._head
        return self

    def __next__(self):
        if self._curr is None:
            raise StopIteration
        data = self._curr.value
        self._curr = self._curr.next
        return data

    def __del__(self):
        self.clear()

    def __delitem__(self, index):
        if index < 0 or index >= self._size:
            raise IndexError("llist.__delitem__(index): index out of range.")
        self.pop(index)

    def __get_node(self, index):
        if index < 0 or index >= self._size:
            raise IndexError("llist.__get_node(index): index out of range.")
        curr = self._head
        for _ in range(index):
            curr = curr.next
        return curr

    def __getitem__(self, index):
        if index < 0 or index >= self._size:
            raise IndexError("llist[index]: index out of range.")
        return self.__get_node(index).value

    def __setitem__(self, index, data):
        if index < 0 or index >= self._size:
            raise IndexError("llist[index]: index out of range.")

        self.__get_node(index).value = data

    def clear(self):
        self._head = None
        self._size = 0

    def find(self, item):
        if not self:
            return -1
        curr = self._head
        idx = 0
        while curr is not None:
            if curr.value == item:
                return idx
            curr = curr.next
            idx += 1
        return -1

    def get(self, index):
        if index < 0 or index >= self._size:
            raise IndexError("llist.get(index): index out of range.")
        return self.__get_node(index).value

    def push(self, data):
        _new = Node(data, next=self._head)
        self._head = _new
        self._size += 1

    def insert(self, index, data):
        if index < 0 or index >= len(self):
            raise IndexError("llist.insert(index, data): index out of range.")
        _curr = _prev = self._head
        for _ in range(index - 1):
            _prev = _curr
            _curr = _curr.next
        _new = Node(data)

        # insert at the end of the list
        if _curr is None:
            _prev.next = _new
        else:
            _next = _curr.next
            # if has any item next to current index
            if _next:
                _new.next = _next
            _curr.next = _new
        self._size += 1

    def append(self, value):
        _new = Node(value)
        if not self:
            self._head = _new
            self._size += 1
            return

        _curr = self._head
        while _curr.next:
            _curr = _curr.next
        _curr.next = _new
        self._size += 1

    def pop(self, index=None):
        if not self:
            raise IndexError("pop from empty LinearList")
        if index is None:
            index = self._size - 1
        if not (0 <= index < len(self)):
            raise IndexError("llist.pop(index): index out of range.")
        if len(self) == 1:
            data = self._head.value
            self.clear()
            return data
        if index == 0:
            data = self._head.value
            self._head = self._head.next
            self._size -= 1
            return data
        _curr = self._head
        for _ in range(index - 1):
            _curr = _curr.next

        data = _curr.next.value
        _curr.next = _curr.next.next
        self._size -= 1
        return data

    def remove(self, value):
        index = self.find(value)
        if index == -1:
            raise ValueError("llist.remove(item): item not in llist")
        self.pop(index)

    def replace(self, index, data):
        if index < 0 or index >= len(self):
            raise IndexError("llist.replace(index, data): index out of range.")
        target = self.__get_node(index)
        target.value = data

    def swap(self, from_i, to_i):
        if from_i == to_i:
            return
        if not (0 <= from_i < len(self)) or not (0 <= to_i < len(self)):
            raise IndexError("llist.swap(from_i, to_i): index out of range.")

        _from, _to = self.__get_node(from_i), self.__get_node(to_i)
        _from.value, _to.value = _to.value, _from.value


class DoublyList(Iter):
    def __init__(self):
        super().__init__()
        self._head = None
        self._tail = None

    def __repr__(self):
        _str = "[ "
        _curr = self._head
        while _curr:
            _str += str(_curr.value) + " "
            _curr = _curr.next
        return _str + "]"

    def __iter__(self):
        self._curr = self._head
        return self

    def __next__(self):
        if self._curr is None:
            raise StopIteration
        data = self._curr.value
        self._curr = self._curr.next
        return data

    def __del__(self):
        self.clear()

    def __get_node(self, index):
        # negative index is allow.
        if not (-len(self) <= index < len(self)):
            raise IndexError("dlist.__get_node(index): index out of range.")

        if index >= 0:
            _curr = self._head
            for _ in range(index):
                _curr = _curr.next
            return _curr
        else:
            _curr = self._tail
            for _ in range(abs(index + 1)):
                _curr = _curr.prev
            return _curr

    def __getitem__(self, index):
        if not (-len(self) <= index < len(self)):
            raise IndexError("dlist[index]: index out of range.")
        if index < 0:
            index += len(self)
        return self.__get_node(index).value

    def __setitem__(self, index, data):
        if not (-len(self) <= index < len(self)):
            raise IndexError("dlist[index]: index out of range.")
        if index < 0:
            index += len(self)
        self.__get_node(index).value = data

    def __delitem__(self, index):
        if not (-len(self) <= index < len(self)):
            raise IndexError("dlist.__delitem__(index): index out of range.")
        self.pop(index)

    def get(self, index):
        if not (-len(self) <= index < len(self)):
            raise IndexError("dlist.get(index): index out of range.")
        return self.__get_node(index).value

    def clear(self):
        self._size = 0
        self._head = None
        self._tail = None

    # add new item at the top
    def push(self, data):
        _new = Node(data, next=self._head)
        if not self:
            self._head = self._tail = _new
            self._size += 1
            return

        _new.prev = _new
        self._head = _new
        self._size += 1

    # add new item at the bottom
    def append(self, value):
        _new = Node(value)
        if not self:
            self._head = self._tail = _new
            self._size += 1
            return

        _prev = self._tail
        _prev.next = _new
        _new.prev = _prev
        self._tail = _new
        self._size += 1

    def insert(self, index, value):
        if index in {0, -len(self)}:  # Insert at the head
            self.push(value)
        elif index >= len(self) or index == -1:  # Insert at the tail
            self.append(value)
        else:
            _new = Node(value)
            if index > 0:
                _curr = self._head
                for _ in range(index):
                    _curr = _curr.next
            else:
                _curr = self._tail
                for _ in range(abs(index + 1)):
                    _curr = _curr.prev
            _new.next = _curr
            _new.prev = _curr.prev
            _curr.prev.next = _new
            _curr.prev = _new

            self._size += 1

    def find(self, item):
        if not self:
            return -1
        _curr = self._head
        for i in range(len(self)):
            if item == _curr.value:
                return i
            _curr = _curr.next
        return -1

    def pop(self, index=None):
        if not self:
            raise IndexError("pop from empty LinearList")
        index = self._size - 1 if index is None else index
        if not (-self._size <= index < self._size):
            raise IndexError("dlist.pop(index): index out of range.")

        if len(self) == 1:
            data = self._head.value
            self.clear()
            return data
        if index == 0:  # Remove head
            data = self._head.value
            self._head = self._head.next
            self._head.prev = None
        elif index == -1 or index == self._size - 1:  # Remove tail
            data = self._tail.value
            self._tail = self._tail.prev
            self._tail.next = None
        else:
            if index > 0:
                _prev = _curr = self._head
                for _ in range(index):
                    _prev = _curr
                    _curr = _curr.next
                _prev.next = _curr.next
                data = _curr.value
            else:
                _prev = _curr = self._tail
                for _ in range(abs(index + 1)):
                    _prev = _curr
                    _curr = _curr.prev
                _curr.prev = _prev.prev
                data = _curr.value
        self._size -= 1
        return data

    def remove(self, value):
        index = self.find(value)
        if index == -1:
            raise ValueError("dlist.remove(item): item not in llist")
        self.pop(index)

    def replace(self, index, data):
        if not (-len(self) <= index < len(self)):
            raise IndexError("dlist.replace(index, data): Index out of range.")
        target = self.__get_node(index)
        target.value = data

    def swap(self, from_i, to_i):
        if from_i == to_i:
            return
        if not (-len(self) <= from_i < len(self)) or not (
            -len(self) <= to_i < len(self)
        ):
            raise IndexError("dlist.swap(from_i, to_i): index out of range.")

        _from, _to = self.__get_node(from_i), self.__get_node(to_i)
        _from.value, _to.value = _to.value, _from.value


def llist(iter: Iterable) -> LinearList:
    if not isinstance(iter, Iterable):
        raise TypeError(
            "LinearList.__init__(iter: iterable) -> LinearList: Expected an iterable object."
        )

    _llist = LinearList()
    for item in iter:
        _llist.append(item)
    return _llist


def dlist(iter: Iterable) -> DoublyList:
    if not isinstance(iter, Iterable):
        raise TypeError(
            "DoublyList.__init__(iter: iterable) -> DoublyList: Expected an iterable object."
        )

    _dlist = DoublyList()
    for item in iter:
        _dlist.append(item)
    return _dlist
