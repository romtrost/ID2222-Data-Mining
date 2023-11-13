class CompareSets:

    def jaccard_similarity(set_1, set_2):
        """ Returns the jaccard similarity between two sets of integers. """

        intersection_size = len(set(set_1) & set(set_2))
        union_size = len(set(set_1) | set(set_2))

        similarity = intersection_size / union_size if union_size != 0 else 0

        return similarity