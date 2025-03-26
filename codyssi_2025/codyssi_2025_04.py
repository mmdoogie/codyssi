from itertools import groupby
import string

from mrm.text import let2num

def parse():
    with open('data/codyssi_2025/04.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return lines

def mem_units(ch):
    if ch in string.digits:
        return int(ch)
    return let2num(ch) + 1

def part1(output=False):
    lines = parse()
    return sum(sum(mem_units(c) for c in l) for l in lines)

def lossy_compress(line):
    keep = len(line) // 10
    remove = len(line) - 2 * keep
    return line[:keep] + str(remove) + line[-keep:]

def part2(output=False):
    lines = parse()
    return sum(sum(mem_units(c) for c in lossy_compress(l)) for l in lines)

def rle_compress(line):
    res = ''
    for let, grp in groupby(line):
        res += let + str(len(list(grp)))
    return res

def part3(output=False):
    lines = parse()
    return sum(sum(mem_units(c) for c in rle_compress(l)) for l in lines)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
    print('Part 3:', part3(True))
