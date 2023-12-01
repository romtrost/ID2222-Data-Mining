import random
from collections import defaultdict
from SubGraph import SubGraph

class TriestImpr:
    """ Implementation of the Triest-Base Algorithm. """

    def __init__(self, m):
        self.subgraph = SubGraph()
        self.m = m
        self.glo_count = 0
        self.loc_count = defaultdict(int)

    def reservoir_sample(self, t):
        """ Samples an edge. """

        if t > self.m:
            # simulates flipping a biased coin with the heads probability M/t
            if random.random() < self.m / t:
                # get random edge from graph
                x, y = random.choice(list(self.subgraph.edges))
                # remove sampled edge from graph
                self.subgraph.rem_edge(x, y)
                return True
            else:
                return False
        else:
           return True

    def update_counters(self, u, v, t):
        """ Update counters. """

        # need edge to contain both points
        if u in self.subgraph.adjency and v in self.subgraph.adjency:

            neighbors = self.subgraph.adjency.get(u) & self.subgraph.adjency.get(v)

            if t*(t-1)*(t-2) / (self.m*(self.m-1)*(self.m-2)) > 1:
                value = t*(t-1)*(t-2) / (self.m*(self.m-1)*(self.m-2))
            else:
                value = 1

            # update the global/local counters
            for neighbor in neighbors:
                self.glo_count += value
                self.loc_count[neighbor] += value
                self.loc_count[u] += value
                self.loc_count[v] += value

    def algorithm(self, stream_edges_dataset):
        """ TRIEST algorithm. """

        t = 0
        for u, v in stream_edges_dataset:
            # make sure this edge is not in our subgraph
            if not (u, v) in self.subgraph.edges:
                t += 1
                self.update_counters(u, v, t)
                is_sampled = self.reservoir_sample(t)
                if is_sampled:
                    self.subgraph.add_edge(u, v)

        # compute global and local triangle count estimates
        glo_triangles = int(self.glo_count)
        loc_triangles = {}
        for node, counter in self.loc_count.items():
            loc_triangles[node] = int(counter)

        return glo_triangles, loc_triangles
