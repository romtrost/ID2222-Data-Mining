import time
import argparse
from DataPreprocessing import read_dataset
from Shingling import Shingling
from MinHashing import MinHashing
from CompareSignatures import CompareSignatures
from LSH import LSH


parser = argparse.ArgumentParser(description='Finding similar documents using Shingling and Minhashing.')
parser.add_argument('-dataset-name', default='News_Category_Dataset_v3.json', help='path to dataset')
parser.add_argument('-num-documents', default=1000, type=int, help='number of documents to read from dataset')
parser.add_argument('-num-shingles', default=3, type=int, help='number of shingles to use')
parser.add_argument('-num-hash-functions', default=100, type=int, help='number of hash functions to use')
parser.add_argument('-use-permutations', default=True, action='store_true', help='use permutations or simple hashing')
parser.add_argument('-num-bands', default=20, type=int, help='number of bands to use in LSH')
parser.add_argument('-threshold', default=0.25, type=float, help='similarity threshold to use')

args = parser.parse_args()
print(args)

shingling = Shingling(args.num_shingles)
minHashing = MinHashing(args.num_hash_functions)
lsh = LSH(args.num_bands, args.threshold)

documents = read_dataset(dataset_name=args.dataset_name, num_documents=args.num_documents)
charMatrix = shingling.create_characteristic_matrix(documents)

if args.use_permutations:
    signature = minHashing.compute_signature_permutation(charMatrix)
else:
    signature = minHashing.compute_signature_hashing(charMatrix)

start_time = time.time()
similarDocuments = lsh.find_similar(signature)
end_time = time.time()

print(f"### Finding similar documents from {args.num_documents} documents... ###")
print(f"### Similar documents -->", similarDocuments)
print(f"### Execution time: {end_time - start_time} seconds")