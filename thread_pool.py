import time, threading


class Pool(object):
	def __init__(self, workers=4):
		# Set up workers
		self._running = True
		self._working = False
		self._work = None
		self._workers = [threading.Thread(target=self._update) for _ in range(workers)]
		for worker in self._workers:
			worker.daemon = True
			worker.start()

	def map(self, values, function):
		assert hasattr(function, '__call__')
		# Set up task
		values = list(values)
		results = [None] * len(values)
		index = 0
		# Define worker task
		def work():
			nonlocal index, values, results
			if index < len(values):
				value = values[index]
				result = function(value)
				results[index] = result
				index += 1
		self._work = work
		# Start processing and wait for result
		self._working = True
		while index < len(values):
			time.sleep(0.01)
		self._working = False
		return results

	def reduce(self, values, function, chunk_size=16):
		# Split input values into chunks
		chunks = []
		current = 0
		while current < len(values):
			upto = min(current + chunk_size, len(values))
			chunks.append(values[current:upto])
			current = upto
		# Call map function to combine values
		reduced = self.map(chunks, function)
		# Reduce recursively until a single value is left
		if len(reduced) == 1:
			return reduced[0]
		return self.reduce(reduced, function, chunk_size)

	def _update(self):
		while self._running:
			if self._working:
				self._work()
			else:
				time.sleep(0.01)


def test(upto=1000):
	def map_function(element):
		return element ** 2

	def reduce_function(elements):
		return sum(elements)

	pool = Pool()
	mapped = pool.map(range(upto), map_function)
	reduced = pool.reduce(mapped, reduce_function)

	summed = 0
	for element in range(upto):
		summed += element ** 2

	assert reduced == summed


if __name__ == '__main__':
	test()
