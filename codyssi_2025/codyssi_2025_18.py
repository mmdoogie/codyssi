from dataclasses import dataclass
from collections import defaultdict
from itertools import product

from mrm.cache import Keycache
from mrm.dijkstra import Dictlike, dijkstra
from mrm.parse import all_nums
import mrm.point as pt

@dataclass
class DebrisRule:
    num: int
    coeffs: tuple
    divisor: int
    remainder: int
    velocity: tuple

    def __init__(self, *args):
        if len(args) != 11:
            raise ValueError("Improper number of numbers")
        self.num = args[0]
        self.coeffs = tuple(args[1:5])
        self.divisor = args[5]
        self.remainder = args[6]
        self.velocity = tuple(args[7:12])

def parse():
    with open('data/codyssi_2025/18.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return [DebrisRule(*all_nums(l)) for l in lines]

DIM_MODS = (10, 15, 60, 3)
DIM_OFFSETS = (0, 0, 0, 1)

def enumerate_debris(rules):
    debris = defaultdict(list)

    for loc in product(*(range(-o, r-o) for r, o in zip(DIM_MODS, DIM_OFFSETS))):
        for r in rules:
            if sum(a * b for a, b in zip(loc, r.coeffs)) % r.divisor == r.remainder:
                debris[loc] += [r]

    return debris

def part1(output=False):
    rules = parse()
    debris = enumerate_debris(rules)

    return sum(len(d) for d in debris.values())

@Keycache(stats=True)
def occupied_at_time(debris, t, *, key):
    occupied = defaultdict(int)

    for d, rules in debris.items():
        for r in rules:
            loc = tuple((i + t * v + o) % m - o for i, v, m, o in zip(d, r.velocity, DIM_MODS, DIM_OFFSETS))
            # optim: only need to record occupied spots on plane a=0 as we can't move to other a planes.
            if loc[3] != 0:
                continue
            occupied[loc] += 1

    return occupied

ADJ_ZERO = [p + (0,) for p in pt.adj_ortho(pt.ZERO_3D)]

@Keycache(stats=True)
def adj_xyz(loc, *, key):
    adj = set()
    for ngh in ADJ_ZERO:
        nloc = tuple(a + b for a, b in zip(loc, ngh))
        skip = False
        for c, m, o in zip(nloc, DIM_MODS, DIM_OFFSETS):
            if c + o < 0 or c + o >= m:
                skip = True
                break
        if not skip:
            adj.add(nloc)
    return adj

def part2(output=False):
    rules = parse()
    debris = enumerate_debris(rules)
    start_pt = (0, 0, 0, 0)
    end_pt = (9, 14, 59, 0)

    def ngh(node):
        loc, t = node
        adj = set()
        occ = occupied_at_time(debris, t + 1, key=t + 1)
        if loc == start_pt or loc not in occ:
            adj.add((loc, t + 1))
        for a in adj_xyz(loc, key=loc):
            if a not in occ:
                adj.add((a, t + 1))
        return adj

    def dist_est(loc):
        return pt.m_dist(end_pt, loc[0])

    w = dijkstra(Dictlike(ngh), start_point=(start_pt, 0), end_fn = lambda pt: pt[0] == end_pt, keep_paths=False, dist_est=dist_est)

    if output:
        hit, miss = occupied_at_time.stats()
        print(f'occupied_at_time cache: {hit+miss} calls: {hit} hits ({hit/(hit+miss)*100:.1f}%), {miss} misses')
        hit, miss = adj_xyz.stats()
        print(f'adj_xyz          cache: {hit+miss} calls: {hit} hits ({hit/(hit+miss)*100:.1f}%), {miss} misses')

    return min(w[k] for k in w if k[0] == end_pt)

def part3(output=False):
    rules = parse()
    debris = enumerate_debris(rules)
    start_pt = (0, 0, 0, 0)
    end_pt = (9, 14, 59, 0)

    occupied_at_time.reset(stats_only=True)
    adj_xyz.reset(stats_only=True)

    def ngh(node):
        loc, t, hits = node
        adj = set()
        occ = occupied_at_time(debris, t + 1, key=t + 1)
        if loc == start_pt:
            adj.add((loc, t + 1, hits))
        if occ[loc] <= hits:
            adj.add((loc, t + 1, hits - occ[loc]))
        for a in adj_xyz(loc, key=loc):
            if occ[a] <= hits:
                adj.add((a, t + 1, hits - occ[a]))
        return adj

    def dist_est(loc):
        return pt.m_dist(end_pt, loc[0])

    w = dijkstra(Dictlike(ngh), start_point=(start_pt, 0, 3), end_fn = lambda pt: pt[0] == end_pt, keep_paths=False, dist_est=dist_est)

    if output:
        hit, miss = occupied_at_time.stats()
        print(f'occupied_at_time cache: {hit+miss} calls: {hit} hits ({hit/(hit+miss)*100:.1f}%), {miss} misses')
        hit, miss = adj_xyz.stats()
        print(f'adj_xyz          cache: {hit+miss} calls: {hit} hits ({hit/(hit+miss)*100:.1f}%), {miss} misses')

    return min(w[k] for k in w if k[0] == end_pt)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
    print('Part 3:', part3(True))
