from tree_print import Node, example_tree


def traverse_depth_first(root):
    """
    Recursively traverse the tree in order using depth first search.
    """
    if root.left:
        yield from traverse_depth_first(root.left)
    yield root.value
    if root.right:
        yield from traverse_depth_first(root.right)


def traverse_breadth_first(root):
    """
    Iteratively traverse the tree using breadth first search.
    """
    queue = [root]
    while queue:
        node = queue.pop(0)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
        yield node.value


def traverse_constant_space(root):
    """
    Iteratively traverse the tree in order with using constant additional
    space over the results list. Makes use of parent pointers.
    """
    elements = []
    node, child = root, None
    while True:
        # Visit left child if existing and not already done
        if node.left and not child:
            node, child = node.left, None
            continue
        # Add value if left was visited or didn't exist
        if child is node.left:
            elements.append(node.value)
        # Visit right node if existing and not already done
        if node.right and child is not node.right:
            node, child = node.right, None
            continue
        # Traverse upwards if we are not the root
        if node.parent:
            node, child = node.parent, node
            continue
        break
    return elements


def print_elements(title, elements):
    title = '{: <18}'.format(title)
    elements = ', '.join(str(x) for x in elements)
    print(title, elements)


if __name__ == '__main__':
    tree = example_tree()
    tree.print()
    print_elements('Depth first', traverse_depth_first(tree))
    print_elements('Constant space', traverse_constant_space(tree))
    print_elements('Breadth first', traverse_breadth_first(tree))
