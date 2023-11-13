import sympy
import numpy as np

class MinHashing:

    def __init__(self, nSignature=500):
        self.nSignature = nSignature

    def compute_signature_hashing(self, charMatrix):
        """ Returns the signature from hashing. """

        nSignature, (nShingles, n_docs) = self.nSignature, charMatrix.shape

        # initialize the signature matrix
        signature = np.full((nSignature, n_docs), np.inf)

        # initialze values for universal hashing
        p = sympy.nextprime(nShingles)
        a = 2 * np.random.randint(0, p//2, nSignature) + 1  # a is always an odd number
        b = np.random.randint(0, p, nSignature)

        # for each shingle
        for shingleID, documentIDs in enumerate(charMatrix.tolil().rows):
            # compute nSignature hash functions
            hashes = ((a*shingleID + b) % p) % nShingles
            # for each document with specific shingle
            for documentID in documentIDs:
                signature[:, documentID] = np.minimum(hashes, signature[:, documentID])

        return signature

    def compute_signature_permutation(self, charMatrix):
        """ Returns the signature from permutation. """

        nSignature, (nShingles, n_docs) = self.nSignature, charMatrix.shape

        # initialize the signature matrix with zeros
        signature = np.zeros((nSignature, n_docs), dtype=np.int32)

        for idx in range(nSignature):
            # permute the rows of the characteristic matrix
            rand_idxs = np.random.permutation(nShingles)
            charMatrix_perm = charMatrix[rand_idxs, :]

            # the minhash is the row-wise position of the first one
            signature[idx, :] = np.argmax(charMatrix_perm, axis=0)

        return signature