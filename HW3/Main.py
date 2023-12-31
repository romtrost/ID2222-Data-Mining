import time
import argparse
from TriestBase import TriestBase
from TriestImpr import TriestImpr
from DataPreprocessing import read_dataset

parser = argparse.ArgumentParser(description='Finding triangle count estimates in a data stream of graph edges using TRIEST.')
parser.add_argument('-dataset-name', default='data/web-Stanford.txt', help='path to dataset')
parser.add_argument('-m', default=10000, type=int, help='how many edge samples to use in reservoir sampling')
parser.add_argument('-t', default='BASE', type=str, help='type of TRIEST algorithm to use: [BASE, IMPR]')

args = parser.parse_args()
print(args)

stream_edges_dataset = read_dataset(args.dataset_name)

triest = TriestBase(args.m) if args.t == 'BASE' else TriestImpr(args.m)

print(f"--- Finding triangle estimates using TRIEST-{args.t} ---")
start_time = time.time()
glo_triangles, loc_triangles = triest.algorithm(stream_edges_dataset)
print(f'Global triangles estimate: {glo_triangles}')
#print(f'Local triangles estimate: {loc_triangles}')
print(f'The algorithm took {time.time() - start_time} seconds.')
