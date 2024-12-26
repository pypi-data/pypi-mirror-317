class Node:
    def __init__(self, data):
        self.data = data
        self._left = None
        self._right = None

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    @left.setter
    def left(self, node):
        self._left = node

    @right.setter
    def right(self, node):
        self._right = node


def preorder(node):
    if node == None:
        return
    print(node.data)
    preorder(node.left)
    preorder(node.right)


def __test_create_node():
    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.left = Node(4)
    root.left.right = Node(5)

    print("Preorder traversal:")
    preorder(root)
