from collections import defaultdict

class SubGraph:
    """ Sub-graph class. """

    def __init__(self):
        """ Initialise sub-graph. """

        self.adjency = defaultdict(set)
        self.edges = set()

    def add_edge(self, u, v):
        """ Add edge to sub-graph. """

        self.adjency[u].add(v)
        self.adjency[v].add(u)
        self.edges.add((u, v))

    def rem_edge(self, u, v):
        """ Remove edge from sub-graph. """

        self.adjency[u].remove(v)
        self.adjency[v].remove(u)
        self.edges.remove((u, v))
        if not self.adjency[u]:
            del self.adjency[u]
        if not self.adjency[v]:
            del self.adjency[v]
