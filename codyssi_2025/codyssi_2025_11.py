import string

def parse():
    with open('data/codyssi_2025/11.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return lines

BASE_CHARS = string.digits + string.ascii_uppercase + string.ascii_lowercase + '!@#$%^'
FWD_VALS = {c: i for i, c in enumerate(BASE_CHARS)}
REV_VALS = {v: k for k, v in FWD_VALS.items()}

def from_base(num, base):
    base = int(base)
    res = 0
    for c in num:
        res += FWD_VALS[c]
        res *= base

    return res // base

def to_base(num, base):
    base = int(base)
    res = ''
    while num:
        res += REV_VALS[num % base]
        num = num // base

    return ''.join(reversed(res))

def part1(output=False):
    lines = parse()
    vals = [from_base(*l.split(' ')) for l in lines]
    return max(vals)

def part2(output=False):
    lines = parse()
    vals = [from_base(*l.split(' ')) for l in lines]
    return to_base(sum(vals), 68)

def part3(output=False):
    lines = parse()
    vals = [from_base(*l.split(' ')) for l in lines]
    return round(sum(vals) ** (1/4))

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
    print('Part 3:', part3(True))
