import random
from collections import defaultdict
from SubGraph import SubGraph

class TriestBase:
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
                self.update_counters(x, y, -1)
                return True
            else:
                return False
        else:
           return True

    def update_counters(self, u, v, value):
        """ Update counters. """

        # need edge to contain both points
        if u in self.subgraph.adjency and v in self.subgraph.adjency:

            neighbors = self.subgraph.adjency.get(u) & self.subgraph.adjency.get(v)

            # update the global/local counters
            for neighbor in neighbors:
                self.glo_count += value
                self.loc_count[neighbor] += value
                self.loc_count[u] += value
                self.loc_count[v] += value

            if value == -1:
                for node in neighbors.union({u, v}):
                    if not self.loc_count[node]:
                        del self.loc_count[node]

            """
            if neighbors:
                print("u:                 ", u)
                print("v:                 ", v)
                print("value:                 ", value)
                print("self.subgraph.adjency.get(u)", self.subgraph.adjency.get(u))
                print("self.subgraph.adjency.get(v)", self.subgraph.adjency.get(v))
                print("neighbors", neighbors)
                print("self.glo_count:    ", self.glo_count)
                print("self.loc_count:    ", self.loc_count)
            """

    def algorithm(self, stream_edges_dataset):
        """ TRIEST algorithm. """

        t = 0
        for u, v in stream_edges_dataset:
            # make sure this edge is not in our subgraph
            #print("t ---------------------------> ", t)
            if not (u, v) in self.subgraph.edges:
                t += 1
                is_sampled = self.reservoir_sample(t)
                #print("is_sampled: ", is_sampled)
                if is_sampled:
                    self.subgraph.add_edge(u, v)
                    self.update_counters(u, v, 1)
            #print("subgraph.adjency:  ", self.subgraph.adjency)
            #print("subgraph.edges:    ", self.subgraph.edges)

        # compute global and local triangle count estimates
        if t*(t-1)*(t-2) / (self.m*(self.m-1)*(self.m-2)) > 1:
            est_t = t*(t-1)*(t-2) / (self.m*(self.m-1)*(self.m-2))
        else:
            est_t = 1

        glo_triangles = int(est_t * self.glo_count)
        loc_triangles = {}
        for node, counter in self.loc_count.items():
            loc_triangles[node] = int(est_t * counter)

        return glo_triangles, loc_triangles
