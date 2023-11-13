import numpy as np
from scipy import sparse

class Shingling:

    def __init__(self, k_shingles=3):
        self.k_shingles = k_shingles

    def create_hashed_shingles(self, document):
        """ Returns the hashed singles for a given document. """

        unhashed_shingles = sorted(set([document[i:(i + self.k_shingles)] for i in range(len(document) - self.k_shingles)]))
        # print("unhashed shingles: ", unhashed_shingles)
        hashed_shingles = [self.hash_shingles(shingle) for shingle in unhashed_shingles]
        # print("hashed shingles: ", hashed_shingles)
        return hashed_shingles

    def hash_shingles(self, shingle):
        """ Hashes a shingle. """

        return sum([pow(100, char_idx) * ord(character) for char_idx, character in enumerate(shingle)]) % (2**32)

    def create_characteristic_matrix(self, documents):
        """ Return characteristic matrix. """

        document_shingles, shingle_idxs = self.create_document_shingles(documents)

        rows, cols, data = [], [], []
        for document_id, shingles in enumerate(document_shingles):
            for shingle in shingles:
                rows.append(shingle_idxs[shingle])
                cols.append(document_id)
                data.append(1)

        characteristic_matrix = sparse.csr_matrix((data, (rows, cols)), shape=(len(shingle_idxs), len(document_shingles)), dtype=np.bool_)

        return characteristic_matrix

    def create_document_shingles(self, documents):
        """ Return shingles for each document """

        shingle_collection = set()
        document_shingles = []

        for document in documents:
            shingles = self.create_hashed_shingles(document)
            document_shingles.append(shingles)
            shingle_collection.update(shingles)

        shingle_idxs = {shingle: idx for idx, shingle in enumerate(sorted(shingle_collection))}

        return document_shingles, shingle_idxs