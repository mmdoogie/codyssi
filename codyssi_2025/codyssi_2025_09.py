from collections import defaultdict

def parse():
    with open('data/codyssi_2025/09.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    acts = {}
    trans = []
    for l in lines:
        if 'HAS' in l:
            a, b = l.split(' HAS ')
            acts[a] = int(b)
        if 'FROM' in l:
            items = l.split(' ')
            trans += [(items[1], items[3], int(items[5]))]
    return acts, trans

def part1(output=False):
    acts, trans = parse()
    for t in trans:
        acts[t[0]] -= t[2]
        acts[t[1]] += t[2]
    return sum(sorted(acts.values())[-3:])

def part2(output=False):
    acts, trans = parse()
    for t in trans:
        amt = t[2]
        if acts[t[0]] < t[2]:
            amt = acts[t[0]]
        acts[t[0]] -= amt
        acts[t[1]] += amt
    return sum(sorted(acts.values())[-3:])

def repay_debts(acts, debts, acct):
    while acts[acct] and debts[acct]:
        debt = debts[acct][0]
        if acts[acct] >= debt[1]:
            amt = debt[1]
        else:
            amt = acts[acct]
        acts[debt[0]] += amt
        acts[acct] -= amt
        debt[1] -= amt
        if debt[1] == 0:
            debts[acct].pop(0)
        repay_debts(acts, debts, debt[0])

def part3(output=False):
    acts, trans = parse()
    debts = defaultdict(list)
    for t in trans:
        amt = t[2]
        if acts[t[0]] < t[2]:
            amt = acts[t[0]]
            debts[t[0]] += [[t[1], t[2] - amt]]
        acts[t[0]] -= amt
        acts[t[1]] += amt

        if debts[t[1]]:
            repay_debts(acts, debts, t[1])
    return sum(sorted(acts.values())[-3:])

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
    print('Part 3:', part3(True))
