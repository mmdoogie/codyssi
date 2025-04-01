from dataclasses import dataclass

from mrm.parse import all_nums

@dataclass
class Material:
    qual: int
    cost: int
    uniq: int

    def __init__(self, qual=0, cost=0, uniq=0):
        self.qual = qual
        self.cost = cost
        self.uniq = uniq

    def p1_key(self):
        return (self.qual, self.cost, self.uniq)

    def p23_key(self):
        return (self.qual, -self.uniq)

    def __add__(self, m2):
        return Material(self.qual + m2.qual, self.cost + m2.cost, self.uniq + m2.uniq)

def parse():
    with open('data/codyssi_2025/14.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return {l.split(' ')[1]: Material(*list(all_nums(l))[1:]) for l in lines}

def part1(output=False):
    matls = parse()
    return sum(m.uniq for m in sorted(matls.values(), reverse=True, key=Material.p1_key)[:5])

def make_costs(matls):
    cost_qual = {}
    for m in matls.values():
        cqu = {m.cost: max(cost_qual[m.cost], m, key=Material.p23_key) if m.cost in cost_qual else m}
        for ck, cv in cost_qual.items():
            cqu[ck + m.cost] = max(cost_qual[ck + m.cost], cv + m, key=Material.p23_key) if ck + m.cost in cost_qual else cv + m
        cost_qual |= cqu
    return cost_qual

def part2(output=False):
    matls = parse()
    cost_qual = make_costs(matls)
    best = cost_qual[30]
    return best.qual * best.uniq

def part3(output=False):
    matls = parse()
    cost_qual = make_costs(matls)
    best = cost_qual[300]
    return best.qual * best.uniq

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
    print('Part 3:', part3(True))
