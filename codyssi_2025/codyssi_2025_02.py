from itertools import dropwhile

def parse():
    with open('data/codyssi_2025/02.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    coeffs = [int(l.split(' ')[-1]) for l in lines[:3]]
    rooms = sorted(int(l) for l in lines[4:])
    return coeffs, rooms

def score(coeffs, room):
    return room ** coeffs[2] * coeffs[1] + coeffs[0]

def part1(output=False):
    coeffs, rooms = parse()
    median = rooms[len(rooms) // 2]
    return score(coeffs, median)

def part2(output=False):
    coeffs, rooms = parse()
    return score(coeffs, sum(r for r in rooms if r % 2 == 0))

def part3(output=False):
    coeffs, rooms = parse()
    MAX_COST = 15000000000000
    max_qual = ((MAX_COST - coeffs[0]) / coeffs[1]) ** (1 / coeffs[2])
    return next(dropwhile(lambda x: x > max_qual, reversed(rooms)))

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
    print('Part 3:', part3(True))

