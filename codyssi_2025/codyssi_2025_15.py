from dataclasses import dataclass
from functools import reduce

@dataclass
class Artifact:
    code: str
    uid: int

    def __init__(self, code, uid):
        self.code = code
        self.uid = int(uid)

def parse():
    with open('data/codyssi_2025/15.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    arts = [Artifact(*l.split(' | ')) for l in lines if l != '']
    return arts[:-2], arts[-2:]

@dataclass
class Node:
    left = None
    right = None
    level = 0
    item: Artifact = None

def make_tree(arts):
    root = Node()
    root.item = arts[0]
    all_nodes = [root]

    for a in arts[1:]:
        all_nodes += [insert_node(root, a)]

    return all_nodes

def insert_node(root, a, trace = False):
    at = root
    path = []
    while True:
        if trace:
            path += [at]
        if a.uid <= at.item.uid:
            if at.left is None:
                ins = Node()
                ins.level = at.level + 1
                ins.item = a
                at.left = ins
                break
            at = at.left
            continue
        if at.right is None:
            ins = Node()
            ins.level = at.level + 1
            ins.item = a
            at.right = ins
            break
        at = at.right
    if trace:
        return ins, path
    return ins

def part1(output=False):
    arts, _ = parse()
    nodes = make_tree(arts)
    max_depth = max(n.level for n in nodes)
    by_level = {l: [n.item.uid for n in nodes if n.level == l] for l in range(max_depth + 1)}
    if output:
        for l in by_level:
            print(f'Level {l:2d}: {len(by_level[l]):3d} items, sum {sum(by_level[l])}')
    return max(sum(l) for l in by_level.values()) * (max_depth + 1)

def part2(output=False):
    arts, _ = parse()
    nodes = make_tree(arts)
    new_art = Artifact('XXX', 500000)
    _, path = insert_node(nodes[0], new_art, trace=True)
    return '-'.join(n.item.code for n in path)

def part3(output=False):
    arts, to_check = parse()
    nodes = make_tree(arts)

    paths = [insert_node(nodes[0], t, trace=True)[1] for t in to_check]
    path_depths = [set((n.level, n.item.code) for n in p) for p in paths]

    if output:
        for p in paths:
            print(f'To {p[-1].item.code}: {"-".join(n.item.code for n in p)}')

    ancestors = reduce(set.intersection, path_depths)
    lowest = max(ancestors)

    return lowest[1]

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
    print('Part 3:', part3(True))
