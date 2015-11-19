import random


class Node:

    __slots__ = ('parent', 'left', 'right', 'value')

    def __init__(self, parent=None, left=None, right=None, value=None):
        self.parent = parent
        self.left = left
        self.right = right
        self.value = value if value else random.randint(1, 9)

    def __repr__(self):
        return str(self.value)

    def print(self):
        levels = self.levels()
        for index, level in enumerate(levels):
            spacing = 2 ** (len(levels) - index) - 1
            large_half = spacing // 2 + 1
            small_half = spacing // 2
            line = ''
            for node in level:
                if node and node.left:
                    line += ' ' * large_half + '_' * small_half
                else:
                    line += ' ' * spacing
                line += str(node.value) if node else '.'
                if node and node.right:
                    line += '_' * small_half + ' ' * large_half
                else:
                    line += ' ' * spacing
                line += ' '
            print(line)

    def levels(self):
        depth = self.depth()
        queue = [(self, 0)]
        levels = [[] for _ in range(depth)]
        while queue:
            current, level = queue.pop(0)
            if current:
                levels[level].append(current)
                queue.append((current.left, level + 1))
                queue.append((current.right, level + 1))
            elif level < depth:
                levels[level].append(None)
                queue.append((None, level + 1))
                queue.append((None, level + 1))
        return levels

    def depth(self):
        left = self.left.depth() if self.left else 0
        right = self.right.depth() if self.right else 0
        return max(left, right) + 1


def example_tree(iterations=5, branch_factor=0.8):
    root = Node()
    queue = [root]
    for _ in range(iterations):
        if not queue:
            break
        current = queue.pop(0)
        if not current.left and random.random() < branch_factor:
            new = Node(current)
            current.left = new
            queue.append(new)
        if not current.right and random.random() < branch_factor:
            new = Node(current)
            current.right = new
            queue.append(new)
    return root


if __name__ == '__main__':
    tree = example_tree()
    tree.print()
