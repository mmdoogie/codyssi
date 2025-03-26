from mrm.dijkstra import Dictlike, dijkstra
import mrm.point as pt

def parse():
    with open('data/codyssi_2025/10.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    grid = [[int(x) for x in l.split(' ')] for l in lines]
    return grid

def part1(output=False):
    grid = parse()
    cols = [sum(l) for l in grid]
    rows = [sum(l[i] for l in grid) for i in range(len(grid[0]))]
    return min(cols, rows)

def part2(output=False):
    grid = parse()
    g = pt.grid_as_dict(grid)

    def ngh(node):
        x, y = node
        return [pt for pt in [(x + 1, y), (x, y + 1)] if pt in g]

    def wt(path):
        _, pt2 = path
        return g[pt2]

    w = dijkstra(Dictlike(ngh), Dictlike(wt), (0, 0), (14, 14), keep_paths=False)
    return w[(14, 14)] + g[(0, 0)]

def part3(output=False):
    grid = parse()
    g = pt.grid_as_dict(grid)

    def ngh(node):
        x, y = node
        return [pt for pt in [(x + 1, y), (x, y + 1)] if pt in g]

    def wt(path):
        _, pt2 = path
        return g[pt2]

    w = dijkstra(Dictlike(ngh), Dictlike(wt), (0, 0), (49, 49), keep_paths=False)
    return w[(49, 49)] + g[(0, 0)]

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
    print('Part 3:', part3(True))
