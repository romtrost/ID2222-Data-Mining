import itertools

class AssociationRules:

    def find(self, L, c):
        """ Generates association rules. """

        # Find association rules by iterating through the levels and keys
        rules = []
        for k in range(2, len(L) + 1):
            for key in L[k].keys():
                for subset in itertools.combinations(key, k - 1):
                    for k1 in key:
                        if k1 not in subset and c <= L[k][key] / L[k - 1][subset]:
                            rules.append([subset, k1, L[k][key] / L[k - 1][subset]])

        return rules
