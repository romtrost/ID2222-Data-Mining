import math
from collections import defaultdict
import itertools
from CompareSignatures import CompareSignatures

class LSH:

    def __init__(self, num_bands=100, threshold=0.8):
        self.num_bands = num_bands
        self.threshold = threshold

    def find_similar(self, signature):
        """ Return similar documents according to threshold. """

        candidate_pairs = self.find_candidates(signature)
        similar_documents = [candidate for candidate in candidate_pairs if self.is_similar(signature, candidate)]

        return similar_documents

    def is_similar(self, signature, candidate):
        """ Check if documents are similar based on threshold. """
        doc_similarity = CompareSignatures.signature_similarity(signature, *candidate)
        return doc_similarity > self.threshold

    def find_candidates(self, signature):
        """ Return candidates to calculate similarity for. """

        num_bands, (n_signature, n_docs) = self.num_bands, signature.shape
        rows_band = math.ceil(n_signature / num_bands)

        candidate_pairs = set()

        for band_idx in range(num_bands):

            band_start, band_end = band_idx * rows_band, (band_idx + 1) * rows_band
            band = signature[band_start:band_end]

            # for each column in this band
            column_buckets = defaultdict(list)
            for doc_id, column in enumerate(band.T):
                column_buckets[tuple(column)].append(doc_id)

            for doc_ids in column_buckets.values():
                pairwise_combinations = itertools.combinations(doc_ids, 2)
                candidate_pairs.update(pairwise_combinations)

        return candidate_pairs