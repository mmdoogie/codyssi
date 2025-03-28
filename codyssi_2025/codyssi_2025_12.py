from collections import deque
from dataclasses import dataclass
from enum import Enum
from itertools import cycle
import string

MODULUS = 1073741824
WIDTH = 30
HEIGHT = 30

class ActionType(Enum):
    SHIFT = 1
    ADD = 2
    MULTIPLY = 3

class ActionScope(Enum):
    ROW = 1
    COLUMN = 2
    ALL = 3

@dataclass
class Action:
    type_: ActionType
    scope: ActionScope
    scope_val: int
    param: int

@dataclass
class GridPoint:
    x: int
    y: int
    val: int

def parse():
    with open('data/codyssi_2025/12.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    grid = []
    acts = []
    patt = []
    scopes = {'ROW': ActionScope.ROW, 'COL': ActionScope.COLUMN, 'ALL': ActionScope.ALL}
    actions = {'ADD': ActionType.ADD, 'SUB': ActionType.ADD, 'MULTIPLY': ActionType.MULTIPLY}
    for l in lines:
        if l == '':
            continue
        if l[0] in string.digits:
            grid += [[int(x) for x in l.split(' ')]]
            continue
        if l in ['TAKE', 'CYCLE', 'ACT']:
            patt += [l]
            continue
        match l.split():
            case ['SHIFT', scope, row, 'BY', amt]:
                amt = int(amt)
                row = int(row) - 1
                acts += [Action(ActionType.SHIFT, scopes[scope], row, amt)]
                continue
            case [action, amt, scope, *val]:
                amt = int(amt)
                val = int(val[0]) - 1 if val else None
                if action == 'SUB':
                    amt *= -1
                acts += [Action(actions[action], scopes[scope], val, amt)]
                continue
    assert len(grid) == HEIGHT
    assert len(grid[0]) == WIDTH
    grid_array = [GridPoint(x, y, grid[y][x]) for x in range(WIDTH) for y in range(HEIGHT)]
    return grid_array, acts, patt

def apply_action(a, grid_array):
    for g in grid_array:
        if a.scope != ActionScope.ALL and (
        (a.scope == ActionScope.ROW and g.y != a.scope_val) or
        (a.scope == ActionScope.COLUMN and g.x != a.scope_val)):
            continue
        if a.type_ == ActionType.SHIFT:
            if a.scope == ActionScope.ROW:
                g.x = (g.x + a.param) % WIDTH
            else:
                g.y = (g.y + a.param) % HEIGHT
        elif a.type_ == ActionType.ADD:
            g.val = (g.val + a.param) % MODULUS
        elif a.type_ == ActionType.MULTIPLY:
            g.val = (g.val * a.param) % MODULUS

def part1(output=False):
    grid, acts, _ = parse()

    for a in acts:
        apply_action(a, grid)

    rows = [sum(g.val for g in grid if g.y == row) for row in range(HEIGHT)]
    cols = [sum(g.val for g in grid if g.x == col) for col in range(WIDTH)]

    return max(rows + cols)

def part2(output=False):
    grid, acts, patt = parse()

    a = deque(acts)
    t = None
    for p in patt:
        match p:
            case 'TAKE':
                t = a.popleft()
                continue
            case 'CYCLE':
                a.append(t)
                continue
            case 'ACT':
                apply_action(t, grid)

    rows = [sum(g.val for g in grid if g.y == row) for row in range(HEIGHT)]
    cols = [sum(g.val for g in grid if g.x == col) for col in range(WIDTH)]

    return max(rows + cols)

def part3(output=False):
    grid, acts, patt = parse()

    a = deque(acts)
    t = None
    for p in cycle(patt):
        if not a:
            break
        match p:
            case 'TAKE':
                t = a.popleft()
                continue
            case 'CYCLE':
                a.append(t)
                continue
            case 'ACT':
                apply_action(t, grid)

    rows = [sum(g.val for g in grid if g.y == row) for row in range(HEIGHT)]
    cols = [sum(g.val for g in grid if g.x == col) for col in range(WIDTH)]

    return max(rows + cols)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
    print('Part 3:', part3(True))
