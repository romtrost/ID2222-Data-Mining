import itertools
import time
from collections import defaultdict

class Apriori:

    def __init__(self, data, s):
        self.data = data
        self.s = s
        self.C_k = defaultdict(int)
        self.L = {}

    def get_candidates(self, L, k):
        """ Generates and returns candidates. """

        L_k = list(L.keys())

        C_k = {}
        for p in L_k:
            for q in L_k:
                if p[:(k-2)] == q[:(k-2)] and q[k-2] > p[k-2]:
                    new_key = p[:(k-1)] + (q[k-2],)
                    C_k[new_key] = 0

        # Prune candidates that have a subset not in L_(k-1)
        remove_list=[c for c in C_k for s in itertools.combinations(c, k-1) if s not in L]
        for i in remove_list:
            C_k.pop(i, None)

        return C_k

    def algorithm(self):
        """ Runs the apriori algorithm. """

        start_time_itemset = time.time()

        basket_list=[]
        with open(self.data, 'r') as f:
            for basket in f:
                items =[]
                for item in basket.split():
                    items.append(int(item))
                basket_list.append(items)
        # print("basket_list", basket_list) # list of lists with each list = basket of items

        # First pass
        for basket in basket_list:
            for item in basket:
                self.C_k[item] += 1

        k = 1
        self.L[k] = {}
        for item in sorted(self.C_k):
            if self.C_k[item] >= self.s:
                self.L[k][(item,)] = self.C_k[item]
        # print("C_k]", self.C_k) # Holds occurences of each item -> {item1: 3201, item2: 200, ...}
        # print("L[k]", self.L[k]) # Keeps items that occur more than support self.s -> {(item1,): 3201, ...}

        # Subsequent passes -> iterate for increasing itemset size until no frequent itemsets are found
        while len(self.L[k]) != 0:

            print("Number of frequent item sets found for k = " + str(k) + " is",  len(self.L[k]), "| execution time:", time.time() - start_time_itemset )
            start_time_itemset=time.time()
            k += 1

            # gets all candidates
            C_k = self.get_candidates(self.L[k-1], k)

            for t in basket_list:
                # For each basket, extract combination of items that are in candidates
                C_t = [c for c in itertools.combinations(t, k) if c in C_k]
                # Add occurence of each found combination
                for c in C_t:
                    C_k[c]+=1
            # print("C_k]", self.C_k) # Holds occurences of each item set -> {(item1, item4): 12, ...}

            # Only keep itemsets that occur at least s times
            self.L[k] = {}
            for item in C_k:
                if C_k[item] >= self.s:
                    self.L[k][item] = C_k[item]

        return self.L

