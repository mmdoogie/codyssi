import string

def parse():
    with open('data/codyssi_2025/06.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return lines[0]

def part1(output=False):
    line = parse()
    return sum(l in string.ascii_letters for l in line)

def part2(output=False):
    line = parse()
    value = {c: i + 1 for i, c in enumerate(string.ascii_lowercase + string.ascii_uppercase)}
    return sum(value[l] for l in line if l in value)

def part3(output=False):
    line = parse()
    value = {c: i + 1 for i, c in enumerate(string.ascii_lowercase + string.ascii_uppercase)}
    prev_val = 0
    tot = 0
    for l in line:
        if l in value:
            prev_val = value[l]
            tot += prev_val
            continue
        prev_val = prev_val * 2 - 5
        if prev_val < 1:
            prev_val += 52
        if prev_val > 52:
            prev_val -= 52
        assert 1 <= prev_val <= 52
        tot += prev_val
    return tot

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
    print('Part 3:', part3(True))
