import time
import argparse
from Apriori import Apriori
from AssociationRules import AssociationRules

parser = argparse.ArgumentParser(description='Finding frequent itemset and association rules.')
parser.add_argument('-dataset-name', default='data/T10I4D100K.dat', help='path to dataset')
parser.add_argument('-s', default=1000, type=int, help='minimum support for an itemset')
parser.add_argument('-c', default=0.5, type=float, help='minimum confidence for a rule')

args = parser.parse_args()
print(args)

print("--- Finding frequent item sets ---")
start_time_apriori = time.time()
apriori=Apriori(data=args.dataset_name, s=args.s)
L_k=apriori.algorithm()
print("Apriori algorithm execution time:", time.time() - start_time_apriori)
# print("L_k", L_k)

print("--- Generating association rules ---")
start_time_rules = time.time()
associationrules=AssociationRules()
rules=associationrules.find(L_k, c=args.c)
for rule in rules:
    print(rule[0], "->", rule[1])
print("Association rules execution time:", time.time() - start_time_rules)