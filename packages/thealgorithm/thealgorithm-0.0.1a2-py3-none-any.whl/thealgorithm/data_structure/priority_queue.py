class PQNode:
    def __init__(self, data, priority=0):
        self.data = data
        self._priority = priority
        self._next = None

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, priority):
        self._priority = priority

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, next):
        self._next = next

    def __repr__(self):
        return f"PriorityQueue({self.priority} {self.data})"


class PQ:
    def __init__(self, head):
        self.head = head

    def is_empty(self):
        return self.head == None

    def enqueue(self, new):
        # insert new data
        if self.is_empty():
            self.head = new
        else:
            if new.priority < self.head.priority:
                new.next = self.head
                self.head = new
            else:
                current = self.head
                while current.next != None and current.next.priority <= new.priority:
                    current = current.next
                new.next = current.next
                current = new

    def dequeue(self):
        # pop the most priority from queue
        if self.is_empty():
            return None
        else:
            current = self.head
            self.head = self.head.next
            return current

    def top(self):
        return self.head

    @classmethod
    def from_iterable(cls, iterable):
        head = None
        for data, priority in iterable:
            if head is None:
                head = PQNode(data, priority)
            else:
                current = head
                while current.next is not None:
                    current = current.next
                current.next = PQNode(data, priority)
        return cls(head)
