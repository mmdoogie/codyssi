def parse():
    with open('data/codyssi_2025/01.txt', encoding = 'utf-8') as f:
        dat = [x.strip('\n') for x in f.readlines()]
    nums = [int(x) for x in dat[:-1]]
    signs = [{'-': -1, '+': 1}[x] for x in dat[-1]]
    return nums, signs

def part1(output = True):
    nums, signs = parse()
    compass = nums[0] + sum(n*s for n, s in zip(nums[1:], signs))
    return compass

def part2(output = True):
    nums, signs = parse()
    compass = nums[0] + sum(n*s for n, s in zip(nums[1:], reversed(signs)))
    return compass

def part3(output = True):
    nums, signs = parse()
    nums = [10 * a + b for a, b in zip(nums[::2], nums[1::2])]
    compass = nums[0] + sum(n*s for n, s in zip(nums[1:], reversed(signs)))
    return compass

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
    print('Part 3:', part3(True))
