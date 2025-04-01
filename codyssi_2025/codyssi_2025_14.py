from mrm.parse import all_nums
from mrm.util import big_pi

def parse():
    with open('data/codyssi_2025/14.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return {l.split(' ')[1]: list(all_nums(l))[1:] for l in lines}

def part1(output=False):
    matls = parse()
    return sum(v[2] for v in sorted(matls.values(), reverse=True)[:5])

def best_from(path, remcost, score, matls, seen):
    scores = []
    for m in matls.keys():
        if m in path:
            continue
        qual, cost, uniq = matls[m]
        if cost <= remcost:
            nextp = path | {m}
            nps = ':'.join(sorted(nextp))
            if nps not in seen:
                seen.add(nps)
                scores += [best_from(path | {m}, remcost - cost, (score[0] + qual, score[1] - uniq), matls, seen)]
    if len(scores) == 0:
        return score
    return max(scores)

def part2(output=False):
    matls = parse()
    seen = set()
    score = best_from(set(), 30, (0, 0), matls, seen)
    print(len(seen))
    return abs(big_pi(score))

def part3(output=False):
    matls = parse()
    seen = set()
    # score = best_from(set(), 300, (0, 0), matls, seen)
    # print(len(seen))
    # return abs(big_pi(score))
    return ''

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
    print('Part 3:', part3(True))
