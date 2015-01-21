class Node(object):
	__slots__ = ('value', 'next')

	def __init__(self, value, next_=None):
		self.value = value
		self.next = next_

	def __repr__(self):
		return str(self.value)


class List(object):
	def __init__(self):
		self._head = None
		self._tail = None

	def append(self, value):
		node = Node(value)
		if not self._head:
			self._head = node
			self._tail = node
		else:
			self._tail.next = node
			self._tail = node

	def __iter__(self):
		current = self._head
		while current:
			yield current
			current = current.next

	def __contains__(self, value):
		for node in self:
			if node.value == value:
				return True
		return False

	def remove(self, value):
		"""Remove the first node with the passed value from the list"""
		# Find parent
		last = None
		for current, last in self._iter_last():
			if current.value == value:
				break
		else:
			raise ValueError('List does not contain the value to remove')
		# Remove by parent
		self._remove(last)

	def remove_node(self, node):
		"""Compare node identity to remove the passed node if it exists in the
		list"""
		# Find parent
		last = None
		for current, last in self._iter_last():
			if current is node:
				break
		else:
			raise ValueError('List does not contain the node to remove')
		# Remove by parent
		self._remove(last)

	def find_circle(self):
		fast = self._head
		slow = self._head.next
		while fast != slow:
			if fast.next is None:
				return None
			fast = fast.next.next
			slow = slow.next
		assert fast == slow
		return fast

	def _iter_last(self):
		current = self._head
		last = None
		while current:
			yield (current, last)
			last = current
			current = current.next

	def _remove(self, last):
		"""Remove the next node right after the passed one from the list"""
		current = last.next
		# Remove head
		if last is None:
			self._head = current.next
		# Remove tail
		elif current == self._tail:
			self._tail = last
		# Remove in between
		else:
			last.next = current.next

	def __repr__(self):
		nodes = []
		circle_start = self.find_circle()
		if circle_start is not None:
			passed = False
			for node in self:
				if node == circle_start:
					if passed:
						break
					else:
						passed = True
				nodes.append(str(node.value))
		else:
			nodes.extend(map(self, str))
		return '[' + ', '.join(nodes) + ']'


# Fill list
l = List()
for i in range(10):
	l.append(i)
# Create circle
third = l._head.next.next
l._tail.next = third
# Print list
print(l)
