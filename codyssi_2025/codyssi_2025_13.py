from collections import defaultdict
from itertools import pairwise

import networkx as nx

from mrm.dijkstra import dijkstra
from mrm.util import big_pi

def parse():
    with open('data/codyssi_2025/13.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    ngh = defaultdict(list)
    wts = {}
    for l in lines:
        path, length = l.split(' | ')
        src, dst = path.split(' -> ')
        ngh[src] += [dst]
        wts[(src, dst)] = int(length)
    return ngh, wts

def part1(output=False):
    ngh, _ = parse()
    w = dijkstra(ngh, start_point='STT', keep_paths=False)
    return big_pi(sorted(w.values(), reverse=True)[:3])

def part2(output=False):
    ngh, wts = parse()
    w = dijkstra(ngh, wts, start_point='STT', keep_paths=False)
    return big_pi(sorted(w.values(), reverse=True)[:3])

def pathlen(path, wts):
    return sum(wts[(a, b)] for a, b in pairwise(path))

def part3(output=False):
    ngh, wts = parse()
    g = nx.DiGraph(ngh)
    c = nx.simple_cycles(g)
    return max(pathlen(x + [x[0]], wts) for x in c)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
    print('Part 3:', part3(True))
