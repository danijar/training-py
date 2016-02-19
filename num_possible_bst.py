import functools


@functools.lru_cache(maxsize=None)
def num_trees(n):
    if n < 3:
        return max(1, n)
    count = 0
    for root in range(n):
        left = num_trees(root)
        right = num_trees(n - root - 1)
        count += left * right
    return count


def reference(n):
    if n < 3:
        return max(1, n)
    count = 1
    for i in range(2, n + 1):
        count *= (n + i) / i
    return int(round(count))


if __name__ == '__main__':
    """
    Compute the number of possible binary search trees that consist of the
    values 1 to n by dynamic programming.
    """
    print('n computed reference')
    for i in range(30):
        print(i, num_trees(i), reference(i))
        assert num_trees(i) == reference(i)
