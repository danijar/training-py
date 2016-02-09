class Graph:

    def __init__(self):
        self.incoming = []
        self.outgoing = []
        self.edges = []
        self.values = []
        self.weights = []

    def __len__(self):
        return len(self.values)

    def __getitem__(self, index):
        return Node(self, index)

    def create(self, value=None):
        index = len(self.values)
        self.values.append(value)
        self.incoming.append(set())
        self.outgoing.append(set())
        return Node(self, index)

    @property
    def nodes(self):
        return (Node(self, i) for i, _ in enumerate(self.values))


class Node:

    __slots__ = ('graph', 'index')

    def __init__(self, graph, index):
        self.graph = graph
        self.index = index

    def __repr__(self):
        return str(self.value)

    def __eq__(self, other):
        return self.index == other.index

    @property
    def value(self):
        return self.graph.values[self.index]

    @property
    def incoming(self):
        indices = self.graph.incoming[self.index]
        nodes = [Node(self.graph, self.graph.edges[x][0]) for x in indices]
        weights = [self.graph.weights[x] for x in indices]
        return list(zip(nodes, weights))

    @property
    def outgoing(self):
        indices = self.graph.outgoing[self.index]
        nodes = [Node(self.graph, self.graph.edges[x][1]) for x in indices]
        weights = [self.graph.weights[x] for x in indices]
        return list(zip(nodes, weights))

    def connect(self, to, weight=None):
        outgoing = (x[0] for x in self.outgoing)
        if to in outgoing:
            edge = outgoing.index(to)
        else:
            edge = len(self.graph.edges)
        self.graph.edges.append((self.index, to.index))
        self.graph.weights.append(weight)
        self.graph.incoming[to.index].add(edge)
        self.graph.outgoing[self.index].add(edge)


if __name__ == '__main__':
    graph = Graph()
    last = graph.create(0)
    for i in range(int(1e6)):
        node = graph.create(i)
    import random
    for i in range(int(1e6)):
        from_ = graph[random.randrange(len(graph))]
        to = graph[random.randrange(len(graph))]
        from_.connect(to)
