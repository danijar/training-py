def digits(number):
    """Generator to iterate over the digits of a number from right to left."""
    while number > 0:
        yield number % 10
        number //= 10


def count_digits_upto(the_number, the_digit):
    """Count the amount of digits d occuring in the numbers from 0 to n
    with runtime complexity of O(log n)."""
    count = 0
    for index, digit in enumerate(digits(the_number)):
        power = pow(10, index)
        decimal = digit * power
        number = the_number % (power)
        count += index * (decimal // 10)
        if digit > the_digit:
            count += pow(10, index)
        elif digit == the_digit:
            count += number + 1
    return count


def count_digits_upto_naive(the_number, the_digit):
    """Naive implementation of the above function useful for testing
    with runtime complexity of O(n * log n)."""
    count = 0
    for number in range(1, the_number + 1):
        for digit in digits(number):
            if digit == the_digit:
                count += 1
    return count


def interactive():
    print('Count the amount of digits d occuring in the numbers from 0 to n')
    while True:
        digit = int(input('d: '))
        range_ = int(input('n: '))
        print('Result:   ', count_digits_upto(range_, digit))
        print('Reference:', count_digits_upto_naive(range_, digit))
        print('')


def test():
    for base in range(1, 10):
        for number in range(1, 1000):
            result = count_digits_upto(number, base)
            result_naive = count_digits_upto_naive(number, base)
            assert result == result_naive


def benchmark(function=count_digits_upto, input_range=range(0, 10000)):
    """Compare algorithm with naive implementation and print timings in CSV format"""
    import time

    def measure(times, function, *args, **kwargs):
        best = None
        for i in range(times):
            start = time.perf_counter()
            result = function(*args, **kwargs)
            duration = time.perf_counter() - start
            best = min(best, duration) if best is not None else duration
        return best

    def measure_all(times, function, *args, **kwargs):
        start = time.process_time()
        for i in range(times):
            function(*args, **kwargs)
        duration = time.process_time() - start
        return duration

    print('input,1,2,3,4,5,6,7,8,9')
    for number in input_range:
        print(number, end='')
        for base in range(1, 10):
            duration = measure(5, function, number, base)
            print(',' + str(duration), end='')
        print('')


if __name__ == '__main__':
    interactive()
