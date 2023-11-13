import numpy as np

class CompareSignatures:

    def signature_similarity(signature, document1, document2):
        """ Returns similarity between two signatures """

        # number of elements with same signature / total number of elements
        similarity = np.mean(signature[:, document1] == signature[:, document2])

        return similarity