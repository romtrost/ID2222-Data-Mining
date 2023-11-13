from DataPreprocessing import read_dataset
from Shingling import Shingling
from CompareSets import CompareSets
from MinHashing import MinHashing
from CompareSignatures import CompareSignatures

# initialise variables
kShingles = 3           # number of shingles
kHashFunctions = 100    # number of hash functions
document0, document1 = 0, 1       # documents to compare
documents = read_dataset(dataset_name="News_Category_Dataset_v3.json", num_documents=10)

print(f"### Comparing documents {document0} and {document1} using {kShingles} shingles and {kHashFunctions} hash functions. ###")
print(f"### Document {document0} -->", documents[document0])
print(f"### Document {document1} -->", documents[document1])

shingling = Shingling(kShingles)

# computing shingles for document0 and document1
shinglesDocument0 = shingling.create_hashed_shingles(documents[document0])
shinglesDocument1 = shingling.create_hashed_shingles(documents[document1])
print("--- Hashed shingles ---")
print(f"Shingles for document {document0} with {kShingles} shingles:", shinglesDocument0)
print(f"Shingles for document {document1} with {kShingles} shingles:", shinglesDocument1)

# comparing sets
jaccardSimilarity = CompareSets.jaccard_similarity(shinglesDocument0, shinglesDocument1)
print("--- Set similarity ---")
print(f"Jaccard similarity between documents 0 and 1 with {kShingles} shingles:", jaccardSimilarity)

charMatrix = shingling.create_characteristic_matrix(documents)
print("--- Characteristic Matrix ---")
print(charMatrix)

minHashing = MinHashing(kHashFunctions)

# computing signatures using characteristic matrix
signatureHash = minHashing.compute_signature_hash(charMatrix)
signaturePerm = minHashing.compute_signature_perm(charMatrix)

# comparing signatures
signatureHashSimilarity = CompareSignatures.signature_similarity(signatureHash, document0, document1)
signaturePermSimilarity = CompareSignatures.signature_similarity(signaturePerm, document0, document1)
print("--- Signature similarity ---")
print(f'Signature hashing similarity between documents {document0} & {document1}:', signatureHashSimilarity)
print(f'Signature permutation similarity between documents {document0} & {document1}:', signaturePermSimilarity)