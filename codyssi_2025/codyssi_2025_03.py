from collections import Counter, defaultdict, deque, namedtuple
from functools import cache, cmp_to_key, partial, reduce
from itertools import combinations, cycle, groupby, pairwise, permutations, product
import math
import operator
import random
import re

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
    with open('data/codyssi_2025/03.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return [[tuple(int(x) for x in r.split('-')) for r in l.split(' ')] for l in lines]

class pile:
    ranges = []

    def __init__(this, add_ranges = None):
        this.ranges = []
        for r in add_ranges:
            this.add_range(*r)

    def add_range(this, start, end):
        this.ranges += [[start, end]]
        this.consolidate()
        return

    def consolidate(this):
        while True:
            del_ranges = None
            add_range = None
            from itertools import combinations
            for a, b in combinations(this.ranges, 2):
                if a[0] > b[1] or b[0] > a[1]:
                    continue
                del_ranges = [a, b]
                add_range = [min(a[0], b[0]), max(a[1], b[1])]
                break
            if del_ranges is None:
                return
            this.ranges.remove(del_ranges[0])
            this.ranges.remove(del_ranges[1])
            this.ranges += [add_range]

    def unique_labels(this):
        return sum(r[1] - r[0] + 1 for r in this.ranges)

    def __add__(this, that):
        p = pile()
        for r in this.ranges:
            p.add_range(r)
        for r in that.ranges:
            p.add_range(r)
        return p

def part1(output=False):
    ranges = parse()
    return sum(sum(pile([r]).unique_labels() for r in rng) for rng in ranges)

def part2(output=False):
    ranges = parse()
    return sum(pile(rng).unique_labels() for rng in ranges)

def part3(output=False):
    ranges = parse()
    return max(pile(a + b).unique_labels() for a, b in pairwise(ranges))

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
    print('Part 3:', part3(True))
