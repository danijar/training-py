class Node:

    __slots__ = ('value', 'left', 'right')

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def treeify(array):
    """
    Build a balanced binary search tree from a sorted array in O(n).
    """
    if not array:
        return None
    median = len(array) // 2
    root = Node(array[median])
    root.left = treeify(array[:median])
    root.right = treeify(array[median + 1:])
    return root


def inorder(node):
    """
    Traverse the values of a tree in order.
    """
    if not node:
        return []
    yield from inorder(node.left)
    yield node.value
    yield from inorder(node.right)


if __name__ == '__main__':
    array = list(range(30))
    tree = treeify(array)
    assert array == list(inorder(tree))
