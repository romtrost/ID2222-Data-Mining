
def read_dataset(dataset_file):
    """ Reads graph dataset and returns both nodes of edge. """

    with open(dataset_file) as data:
        for line in data:
            elems = line.split()
            # skip comments
            if elems[0] == '#':
                continue
            else:
                # ensure we have edges (i.e: 2 points)
                if len(elems) == 2:
                    src_node, dst_node = int(elems[0]), int(elems[1])
                    if src_node > dst_node:
                        dst_node, src_node = src_node, dst_node
                    yield src_node, dst_node
