class Entry(object):
	"""Entry for the custom dictionary class. Provides an unlimited sequence of
	hash values useful for the collision resolution strategy double hashing."""
	__slots__ = ('key', 'value', '_hash1', '_hash2')

	def __init__(self, key, value):
		self.key = key
		self.value = value
		self._hash1 = self._get_hash1(key)
		self._hash2 = self._get_hash2(key)

	def _get_hash1(self, key):
		value = hash(key)
		value &= 0b1111111111111111
		return value

	def _get_hash2(self, key):
		constant = 0b1011000100111010
		value = hash((37 * hash(key)) ^ constant)
		value &= 0b1111111111111111
		return value

	def hash(self, iteration=0):
		# Combine both hashes based on iteration count
		# TODO: Check if raising the power becomes too slow
		value = (self._hash1 // (iteration + 1)) + (self._hash2 ** iteration)
		value &= 0b1111111111111111
		return value


class Tombstone(object):
	"""Represents a place in the data array of a dictionary that has been
	emptied. This is needed since the dictionary has to continue looking for
	collided entries."""
	__slots__ = ()


class Dictionary(object):
	"""Custom dictionary implemented as a hash table. Supports standard syntax
	for insertion, checking, finding and removing. Don't use this in production
	since Python's dict() is much faster and complete."""
	# Number of tolerated collisions in a row before the underlying array grows
	MAX_TRIES = 10

	def __init__(self):
		self._reserved = 32
		# Initialize underlying array with empty places
		self._data = [None] * self._reserved

	def __setitem__(self, key, value):
		# This entry will be inserted into the underlying array
		entry = Entry(key, value)
		# Use last bits of hash that cover the reserved range
		# Find an empty place using dual hashing
		index = None
		collisions = 0
		for _ in range(Dictionary.MAX_TRIES):
			index = entry.hash(collisions) % self._reserved
			if not isinstance(self._data[index], Entry):
				break
			collisions += 1
		else:
			# TODO: Instead, grow underlying array and copy over entries
			raise UserWarning('Looking up empty place was aborted')
		# Insert entry
		self._data[index] = entry

	def __getitem__(self, key):
		# Get entry and return its value or raise key error
		index = self._get_index(key)
		entry = self._data[index]
		return entry.value

	def __delitem__(self, key):
		# Get index and mark the corresponding place in the underlying array as
		# tombstone or raise key error
		index = self._get_index(key)
		self._data[index] = Tombstone()

	def __contains__(self, key):
		# Dummy entry to get hashes from
		hasher = Entry(key, None)
		# Look for entry with given key
		# Ignore tombstones but stop at empty places
		collisions = 0
		for _ in range(Dictionary.MAX_TRIES):
			index = hasher.hash(collisions) % self._reserved
			entry = self._data[index]
			if not entry:
				return False
			if isinstance(entry, Entry) and entry.key == key:
				return True
			collisions += 1
		else:
			# TODO: Instead, grow underlying array and copy over entries
			raise UserWarning('Looking up key was aborted')

	def __iter__(self):
		for index, entry in enumerate(self._data):
			if isinstance(entry, Entry):
				yield entry.key

	def _get_index(self, key):
		# Dummy entry to get hashes from
		hasher = Entry(key, None)
		# Look for entry with given key
		# Ignore tombstones but stop at empty places
		index = None
		collisions = 0
		for _ in range(Dictionary.MAX_TRIES):
			index = hasher.hash(collisions) % self._reserved
			entry = self._data[index]
			if not entry:
				raise KeyError()
			if isinstance(entry, Entry) and entry.key == key:
				break
			collisions += 1
		else:
			# TODO: Instead, grow underlying array and copy over entries
			raise UserWarning('Looking up key was aborted')
		# Return entry
		return index


def test():
	import random, string

	def assert_equals(one, two):
		for key in one:
			assert key in two
			assert one[key] == two[key]
		for key in two:
			assert key in one
			assert two[key] == one[key]

	def print_pairs(dictionary):
		for key in dictionary:
			print(str(key) + ':', dictionary[key])

	def random_string(length=16):
		letters = string.ascii_lowercase
		choises = [random.choice(letters) for _ in range(length)]
		return ''.join(choises)

	def random_key(dictionary):
		return random.choice(list([key for key in dictionary]))

	# Create both custom and standard library dictionary to compare their
	# behaviors
	custom = Dictionary()
	normal = dict()
	# Test implementation in some insert delete cycles
	for _ in range(5):
		# Fill in some data
		for _ in range(10):
			key = random_string()
			value = random.randint(0, 1000)
			custom[key] = value
			normal[key] = value
		assert_equals(custom, normal)
		# Remove some data
		for _ in range(7):
			key = random_key(custom)
			del custom[key]
			del normal[key]
		assert_equals(custom, normal)
	# Print both dictionaries
	print('Custom dictionary\n-----------------')
	print_pairs(custom)
	print('')
	print('Standard library dict()\n-----------------------')
	print_pairs(normal)
	print('')


if __name__ == '__main__':
	test()
