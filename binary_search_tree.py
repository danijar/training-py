class Entry(object):
	__slots__ = ('left', 'right', 'value')

	def __init__(self, value):
		self.value = value
		self.left = None
		self.right = None


class BinarySearchTree(object):
	def __init__(self):
		self._root = None

	def insert(self, value):
		"""Insert a value into the tree if it doesn't exist"""
		parent, found = self._find_parent(value)
		if found:
			raise ValueError()
		entry = Entry(value)
		if not parent:
			self._root = entry
		elif value < parent.value:
			parent.left = entry
		else:
			parent.right = entry

	def remove(self, value):
		"""Remove value from tree if it exists"""
		parent, found = self._find_parent(value)
		if not found:
			raise ValueError()
		if not parent:
			self._root = None
		elif value < parent.value:
			parent.left = None
		else:
			parent.right = None

	def __contains__(self, value):
		"""Check if value exists in the tree"""
		parent, found = self._find_parent(value)
		return found

	def __iter__(self):
		"""Iterate over values of the tree in sorted order"""
		yield from self._iter(self._root)

	def _iter(self, entry):
		if entry.left:
			yield from self._iter(entry.left)
		yield entry.value
		if entry.right:
			yield from self._iter(entry.right)

	def _find_parent(self, value):
		"""Traverse tree until a parent is found that holds or could hold the
		value. Return boolean as second return value indicating whether the
		value was found."""
		current = self._root
		last = None
		while current:
			if value == current.value:
				return last, True
			if value < current.value:
				last = current
				current = current.left
			else:
				last = current
				current = current.right
		return last, False


def test():
	import random
	tree = BinarySearchTree()
	values = []
	for _ in range(100):
		value = random.randint(0, 99)
		if value not in tree:
			tree.insert(value)
			values.append(value)
	assert list(tree) == sorted(values)


if __name__ == '__main__':
	test()
