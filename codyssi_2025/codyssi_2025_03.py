from itertools import combinations, pairwise

def parse():
    with open('data/codyssi_2025/03.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return [[tuple(int(x) for x in r.split('-')) for r in l.split(' ')] for l in lines]

class pile:
    ranges = []

    def __init__(self, add_ranges = None):
        self.ranges = []
        for r in add_ranges:
            self.add_range(*r)

    def add_range(self, start, end):
        self.ranges += [[start, end]]
        self.consolidate()

    def consolidate(self):
        while True:
            del_ranges = None
            add_range = None
            for a, b in combinations(self.ranges, 2):
                if a[0] > b[1] or b[0] > a[1]:
                    continue
                del_ranges = [a, b]
                add_range = [min(a[0], b[0]), max(a[1], b[1])]
                break
            if del_ranges is None:
                return
            self.ranges.remove(del_ranges[0])
            self.ranges.remove(del_ranges[1])
            self.ranges += [add_range]

    def unique_labels(self):
        return sum(r[1] - r[0] + 1 for r in self.ranges)

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
