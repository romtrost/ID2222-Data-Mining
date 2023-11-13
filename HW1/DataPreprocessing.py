import json
import os

def read_json(data_path: str):
    """ Read and return a json file. """

    if not os.path.exists(data_path):
        print(f"File {data_path} does not exist!")
        return None

    result = []
    with open(data_path) as json_file:
        for line in json_file:
            try:
                # Parse each line as a separate JSON object
                json_object = json.loads(line)
                result.append(json_object)
            except json.decoder.JSONDecodeError as e:
                print(f"Error decoding JSON in file {data_path}: {e}")
                return None

    return result


def read_dataset(dataset_name, num_documents):
    """ Read and return a dataset, returns a list of size num_documents."""

    data_path = os.path.join('data', dataset_name)
    # print(data_path)
    dataset_json = read_json(data_path)
    # print(dataset_json[42])

    documents = []
    for document_idx in range(num_documents):
        documents.append(dataset_json[document_idx]['short_description'])

    return documents