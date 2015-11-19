from list import random_list


def digit_list_to_number(head):
    number = 0
    node = head
    while node:
        number *= 10
        number += node.value
        node = node.next
    return number


def sum_digit_lists(left, right):
    left = digit_list_to_number(left)
    right = digit_list_to_number(right)
    return left + right


def print_aligned(prefix, number):
    print(prefix, '{: >8}'.format(number))


if __name__ == '__main__':
    left = random_list()
    right = random_list()
    print_aligned(' ', ''.join(str(x.value) for x in left))
    print_aligned('+', ''.join(str(x.value) for x in right))
    sum_ = sum_digit_lists(left, right)
    print_aligned('=', sum_)
