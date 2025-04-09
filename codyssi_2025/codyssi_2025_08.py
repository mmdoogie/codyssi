import string

def parse():
    with open('data/codyssi_2025/08.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return lines

def part1(output=False):
    lines = parse()
    return sum(l in string.ascii_lowercase for ll in lines for l in ll)

def reduce_line(line, hyphen=True, output=False):
    charset = string.ascii_lowercase + ('-' if hyphen else '')
    red = True
    if output:
        print('>>> ', line)
    while red:
        red = False
        for i in range(len(line) - 1):
            a = line[i]
            b = line[i + 1]
            if (a in string.digits and b in charset) or (b in string.digits and a in charset):
                red = True
                line = line[:i] + line[i + 2:]
                break
    if output:
        print('<<<', line)
    return line

def part2(output=False):
    lines = parse()
    return sum(len(reduce_line(l, output=output)) for l in lines)

def part3(output=False):
    lines = parse()
    return sum(len(reduce_line(l, hyphen=False, output=output)) for l in lines)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
    print('Part 3:', part3(True))
