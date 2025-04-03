from dataclasses import dataclass
from functools import reduce

from mrm.cache import Keycache
from mrm.parse import all_nums

@dataclass(frozen=True)
class Stair:
    num: int
    start: int
    end: int
    stair_from: int = -1
    stair_to: int = -1

@dataclass(frozen=True)
class Step:
    stair: Stair
    step: int

    def __repr__(self):
        return f'S{self.stair.num}_{self.step}'

    def __lt__(self, s2):
        if self.stair == s2.stair:
            return self.step < s2.step
        return self.stair.num < s2.stair.num

def parse():
    with open('data/codyssi_2025/17.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    stairs = {}
    for l in lines[:-2]:
        nums = list(all_nums(l))
        stairs[nums[0]] = Stair(*nums)
    return stairs, list(all_nums(lines[-1]))

@Keycache(stats=True)
def adj(stairs, all_steps, from_step, **kwargs):
    r = set()

    # check same stair
    if from_step.step + 1 in all_steps[from_step.stair.num]:
        r.add(all_steps[from_step.stair.num][from_step.step + 1])

    # check entering parallel
    dests = filter(lambda s: from_step.step == s.start and from_step.stair.num == s.stair_from, stairs.values())
    for d in dests:
        r.add(all_steps[d.num][from_step.step])

    # check exiting parallel
    if from_step.step == stairs[from_step.stair.num].end and stairs[from_step.stair.num].stair_to != -1:
        r.add(all_steps[stairs[from_step.stair.num].stair_to][from_step.step])

    return r

def reachable(stairs, all_steps, from_step, moves):
    rr = set()
    for m in moves:
        r = set([from_step])

        for _ in range(m):
            r = reduce(set.union, (adj(stairs, all_steps, s, key=s) for s in r), set())
        rr.update(r)
    return rr

@Keycache(stats=True)
def ways_from(stairs, all_steps, moves, start_point, **kwargs):
    tgt = all_steps[1][stairs[1].end]
    if start_point == tgt:
        return 1

    r = reachable(stairs, all_steps, start_point, moves)
    return sum(ways_from(stairs, all_steps, moves, rr, key=rr) for rr in r)

def part1(output=False):
    stairs, moves = parse()

    stairs = {1: stairs[1]}
    all_steps = {s.num:  {p: Step(s, p) for p in range(s.start, s.end + 1)} for s in stairs.values()}

    all_ways = ways_from(stairs, all_steps, moves, all_steps[1][stairs[1].start], key=all_steps[1][stairs[1].start])

    # Part 1 stairs params are different and not included in key, must reset cache in case Part 2/3 run afterwards
    adj.reset()
    ways_from.reset()

    return all_ways

def part2(output=False):
    stairs, moves = parse()

    all_steps = {s.num:  {p: Step(s, p) for p in range(s.start, s.end + 1)} for s in stairs.values()}
    all_ways = ways_from(stairs, all_steps, moves, all_steps[1][stairs[1].start], key=all_steps[1][stairs[1].start])

    return all_ways

def part3(output=False):
    stairs, moves = parse()

    all_steps = {}
    all_steps = {s.num:  {p: Step(s, p) for p in range(s.start, s.end + 1)} for s in stairs.values()}

    at = all_steps[1][stairs[1].start]
    tgt = all_steps[1][stairs[1].end]

    goal = 100000000000000000000000000000 - 1
    offset = 0
    path = [at]

    while True:
        if output:
            print(f'Selected {at}')
        r = reachable(stairs, all_steps, at, moves)

        csum = 0
        for rr in sorted(r):
            w = ways_from(stairs, all_steps, moves, rr, key=rr)
            if output:
                print(f'{rr} has {w} ways to end ({offset + csum} to {offset + csum + w - 1})')

            if goal < offset + csum + w or (rr == tgt and offset + csum == goal):
                at = rr
                path += [rr]
                offset += csum
                break
            csum += w
            if w == 0:
                csum += 1

        if at == tgt:
            if output:
                print(f'Selected {at}')
            break

    if output:
        hit, miss = adj.stats()
        print(f'adj       cache: {hit+miss} calls: {hit} hits ({hit/(hit+miss)*100:.1f}%), {miss} misses')
        hit, miss = ways_from.stats()
        print(f'ways_from cache: {hit+miss} calls: {hit} hits ({hit/(hit+miss)*100:.1f}%), {miss} misses')

    return '-'.join(str(p) for p in path)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
    print('Part 3:', part3(True))
