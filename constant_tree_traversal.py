from print_ascii_tree import Node, example_tree


def traverse(root):
    """
    Traverse the tree in order with using constant space except for the results
    list.
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


if __name__ == '__main__':
    tree = example_tree()
    tree.print()
    elements = traverse(tree)
    print('')
    print(', '.join(str(x) for x in elements))
