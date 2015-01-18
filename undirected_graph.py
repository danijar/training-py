class Node(object):
	def __init__(self, index, graph):
		self._index = index
		self._graph = graph

	def value(self):
		"""Get the value of this node"""
		# This may also be done inside a __getattribute__ method to simplify
		# the interface
		return self._graph._nodes[self._index]

	def __getitem__(self, to, fallback=None):
		"""Get value of edge from this node to the one passed in"""
		to = self._graph._find_node(to)
		if to not in self._graph._connections[self._index]:
			return fallback
		edge = self._graph._connections[self._index][to]
		return self._graph._edges[edge]

	def __setitem__(self, to, value):
		"""Create of update the value of an edge between this node and the one
		passed in"""
		to = self._graph._find_node(to)
		if to in self._graph._connections[self._index]:
			# Update existing edge
			edge = self._graph._connections[self._index][to]
			self._graph._edges[edge] = value
		else:
			# Create new edge
			self._graph._edges.append(value)
			edge = len(self._graph._edges) - 1
			self._graph._connections[self._index][to] = edge
			self._graph._connections[to][self._index] = edge
		print('Set edge between', self._graph._nodes[self._index], 'and',
			self._graph._nodes[to], 'to', self._graph._edges[edge])

	def __delitem__(self, to):
		"""Delete the edge between this node and the one passed in"""
		to = self._graph._find_node(to)
		edge = self._graph._connections[self._index][to]
		del self._graph._connections[self._index][to]
		del self._graph._connections[to][self._index]
		self._graph._edges[edge] = Tombstone()

	def __contains__(self, to):
		"""Check if there is an edge between this node and the one passed in"""
		return to in self._graph._connections[self._index][to]

	def __iter__(self):
		"""Iterate over all nodes connected to this node"""
		for node in self._graph._connections[self._index]:
			yield Node(node, self._graph)

	def edges(self):
		"""Iterate over the values of all edges connected to this node"""
		for node in self._graph._connections[self._index]:
			edge = self._graph._connections[self._index][node]
			if not isinstance(edge, Tombstone):
				yield self._graph._edges[edge]


class Tombstone(object):
	pass


class Graph(object):
	def __init__(self):
		# Values of the nodes and edges
		self._nodes = []
		self._edges = []
		# Node index array of sets holding edge indices
		self._connections = []

	def __getitem__(self, node):
		"""Get node object of the graph from node index, node object or node
		value"""
		node = self._find_node(node)
		return Node(node, self)

	def add(self, value):
		"""Add passed in value as node to the graph and return graph object"""
		assert len(self._nodes) == len(self._connections)
		self._nodes.append(value)
		self._connections.append(dict())
		node = len(self._nodes) - 1
		return self[node]

	def __setitem__(self, node, value):
		"""Set node value of the graph from node index, node object or node
		value"""
		node = self._find_node(node)
		self._nodes[node] = value

	def __delitem__(self, node):
		"""Delete a node and all its edges from the graph"""
		node = self._find_node(node)
		self._nodes[node] = Tombstone()
		# Delete all edges of the node
		edges = self._connections[node]
		for edge in self._connections[node]:
			to = self._edges[edge]
			del self._connections[node][to]
			del self._connections[to][node]
			del self._edges[edge]
		del self._connections[node]

	def __contains__(self, node):
		"""Check if node is an existing node index, node object or node value
		in the graph"""
		node = self._find_node(node)
		return 0 <= node < len(self._nodes)

	def __iter__(self):
		"""Iterate over all edge objects of the graph"""
		for node in range(len(self._nodes)):
			if not isinstance(self._nodes[node], Tombstone):
				yield Node(node, self)

	def _find_node(self, node):
		"""Find a node index from node index, node object or node value"""
		if isinstance(node, int) and node < len(self._nodes):
			return node
		elif isinstance(node, Node):
			return node._index
		elif node in self._nodes:
			return self._nodes.index(node)
		raise KeyError()


def test():
	graph = Graph()
	# Create nodes
	graph.add('A')
	graph.add('B')
	graph.add('C')
	graph.add('D')
	# Add some edges, direction doesn't matter
	graph['A']['B'] = 10
	graph['C']['A'] = 20
	graph['D']['A'] = 30
	# Delete an edge
	del graph['A']['C']
	# Increment and print edges
	result = []
	for node in graph['A']:
		graph['A'][node] += 1
		result.append((node.value(), graph['A'][node]))
	assert result == [('B', 11), ('D', 31)]

if __name__ == '__main__':
	test()
