from list import random_list


def remove_duplicates(head):
    seen = set([head.value])
    previous, node = head, head.next
    while node:
        if node.value in seen:
            node.value = None
            node = node.next
            previous.next = node
        else:
            seen.add(node.value)
            previous = node
            node = node.next
    return head


def remove_duplicates_slow(array):
    seen = set()
    result = []
    for node in array:
        if node.value not in seen:
            result.append(node)
            seen.add(node.value)
    return result


if __name__ == '__main__':
    head = random_list(20)
    unique = remove_duplicates(head)
    reference = remove_duplicates_slow(list(head))
    unique = list(x.value for x in unique)
    reference = list(x.value for x in reference)
    print('Output:   ', unique)
    print('Reference:', reference)
    assert unique == reference

