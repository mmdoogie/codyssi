import mrm.point as pt

def parse():
    with open('data/codyssi_2025/05.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return [tuple(int(v) for v in l.strip('()').split(', ')) for l in lines]

def part1(output=False):
    isles = parse()
    dists = [pt.m_dist((0, 0), i) for i in isles]
    return max(dists) - min(dists)

def part2(output=False):
    isles = sorted(parse())
    dists = [pt.m_dist((0, 0), i) for i in isles]
    closest = isles[dists.index(min(dists))]
    dists = [pt.m_dist(closest, i) for i in isles if i != closest]
    return min(dists)

def part3(output=False):
    isles = sorted(parse())

    at_isle = (0, 0)
    tot = 0
    while len(isles) > 1:
        if at_isle in isles:
            isles.remove(at_isle)
        dists = [pt.m_dist(at_isle, i) for i in isles]
        tot += min(dists)
        at_isle = isles[dists.index(min(dists))]

    return tot

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
    print('Part 3:', part3(True))
