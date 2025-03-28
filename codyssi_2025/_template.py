from dataclasses import dataclass
from collections import Counter, defaultdict, deque, namedtuple
from enum import Enum
from functools import cache, cmp_to_key, partial, reduce
from itertools import combinations, cycle, groupby, pairwise, permutations, product
import math
import operator
import random
import re
import string

import mrm.ansi_term as ansi
from mrm.bitvector import Bitvector
from mrm.cache import Keycache
import mrm.cpoint as cpt
from mrm.crt import all_coprime, coprime, crt
from mrm.dijkstra import Dictlike, dijkstra
from mrm.graph import bfs_dist, bfs_min_paths, connected_component, prim_mst
import mrm.image as img
from mrm.iter import batched, flatten_lists, sliding_window
import mrm.llist as llist
from mrm.parse import all_nums, ensure_equal_length
import mrm.point as pt
from mrm.search import fn_binary_search
from mrm.text import let2num, num2let
from mrm.tsp import held_karp, held_karp_dist
from mrm.util import big_pi, Funkydict, md5sum

def parse():
    with open('data/codyssi_2025/xx.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return lines

def part1(output=False):
    lines = parse()
    return ''

def part2(output=False):
    lines = parse()
    return ''

def part3(output=False):
    lines = parse()
    return ''

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
    print('Part 3:', part3(True))
