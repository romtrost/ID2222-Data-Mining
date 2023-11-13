import argparse
from DataPreprocessing import read_dataset
from Shingling import Shingling
from CompareSets import CompareSets
from MinHashing import MinHashing
from CompareSignatures import CompareSignatures


parser = argparse.ArgumentParser(description='Finding similar documents using Shingling and Minhashing.')
parser.add_argument('-dataset-name', default='News_Category_Dataset_v3.json', help='path to dataset')
parser.add_argument('-num-documents', default=100, type=int, help='number of documents to read from dataset')
parser.add_argument('-document-1', default=0, type=int, help='first document to use for similarity comparison')
parser.add_argument('-document-2', default=1, type=int, help='second document to use for similarity comparison')
parser.add_argument('-num-shingles', default=3, type=int, help='number of shingles to use')
parser.add_argument('-num-hash-functions', default=100, type=int, help='number of hash functions to use')
parser.add_argument('-use-permutations', default=False, action='store_true', help='use permutations or simple hashing')

args = parser.parse_args()
print(args)

shingling = Shingling(args.num_shingles)
minHashing = MinHashing(args.num_hash_functions)

documents = read_dataset(dataset_name=args.dataset_name, num_documents=args.num_documents)
charMatrix = shingling.create_characteristic_matrix(documents)

if args.use_permutations:
    signature = minHashing.compute_signature_perm(charMatrix)
else:
    signature = minHashing.compute_signature_hash(charMatrix)

similarity = CompareSignatures.signature_similarity(signature, args.document_1, args.document_2)

print(f"### Comparing documents {args.document_1} and {args.document_2} using {args.num_shingles} shingles and {args.num_hash_functions} hash functions with permutations = {args.use_permutations}. ###")
print(f"### Document {args.document_1}:", documents[args.document_1])
print(f"### Document {args.document_2}:", documents[args.document_2])
print(f"### Similarity -->", similarity)

