import random


class Element:

    def __init__(self, next=None, value=None):
        self.next = next
        self.value = value or random.randint(1, 9)

    def __iter__(self):
        current = self
        while current:
            yield current
            current = current.next

    def __repr__(self):
        return str(self.value)


def random_list(length=7):
    if length < 1:
        return None
    head = Element()
    current = head
    for _ in range(length - 1):
       current.next = Element()
       current = current.next
    return head
