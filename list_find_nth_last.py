from list import random_list


def find_nth_last(head, n=0):
    behind, current = head, head
    for _ in range(n):
        if not current:
            raise IndexError
        current = current.next
    while current.next:
        current = current.next
        behind = behind.next
    return behind


if __name__ == '__main__':
    length = 7
    head = random_list(7)
    elements = [find_nth_last(head, x).value for x in range(length)]
    elements = list(reversed(elements))
    reference = list(x.value for x in head)
    print('Input: ', reference)
    print('Result:', elements)
    assert elements == reference
