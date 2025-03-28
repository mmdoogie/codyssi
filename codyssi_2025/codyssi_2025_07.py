from itertools import pairwise

def parse():
    with open('data/codyssi_2025/07.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    freqs = [int(l) for l in lines[:-1] if l != '' and '-' not in l]
    swaps = [tuple(int(x) for x in l.split('-')) for l in lines if '-' in l]
    track = int(lines[-1])
    fdict = {i + 1: f for i, f in enumerate(freqs)}
    return fdict, swaps, track

def part1(output=False):
    freqs, swaps, track = parse()
    for s in swaps:
        freqs[s[0]], freqs[s[1]] = freqs[s[1]], freqs[s[0]]
    return freqs[track]

def part2(output=False):
    freqs, swaps, track = parse()
    for s, t in pairwise(swaps):
        freqs[s[1]], freqs[t[0]], freqs[s[0]] = freqs[s[0]], freqs[s[1]], freqs[t[0]]
    return freqs[track]

def part3(output=False):
    freqs, swaps, track = parse()
    track_cnt = len(freqs)
    for s in swaps:
        block_len = min(abs(s[1] - s[0]), track_cnt - max(s))
        for i in range(block_len):
            freqs[s[0] + i], freqs[s[1] + i] = freqs[s[1] + i], freqs[s[0] + i]
    return freqs[track]

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
    print('Part 3:', part3(True))
