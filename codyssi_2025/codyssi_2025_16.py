from dataclasses import dataclass
from enum import Enum
from itertools import zip_longest

import mrm.cpoint as cpt
from mrm.parse import all_nums
from mrm.util import big_pi

GRID_SIZE = 80

class Scope(Enum):
    FACE = 0
    COL = 1
    ROW = 2

@dataclass
class Instr:
    scope: Scope
    scope_val: int
    param: int

    @staticmethod
    def from_line(line):
        s = Scope[line.split(' ')[0]]
        v = list(all_nums(line))
        if s == Scope.FACE:
            return Instr(s, 0, v[0])
        return Instr(s, *v)

def parse():
    with open('data/codyssi_2025/16.txt', 'r', encoding='utf8') as f:
        lines = [l.strip('\n') for l in f.readlines()]
    return [Instr.from_line(l) for l in lines[:-2]], lines[-1]

def blank_grid():
    nodes = {}
    for f in range(6):
        nodes[f] = {}
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                nodes[f][(x, y)] = 0
    return nodes

@dataclass
class Face:
    absorp: int = 0
    rot: complex = cpt.RIGHT

def noop(x):
    return x

def apply_inst(nodes, faces, i, line_ext=False):
    if i.scope == Scope.FACE:
        for n in nodes[0]:
            nodes[0][n] = (nodes[0][n] + i.param) % 100
        faces[0].absorp += GRID_SIZE * GRID_SIZE * i.param
        return

    ext_faces = [0]
    ext_rot = [noop]

    if line_ext:
        if i.scope == Scope.COL:
            ext_faces += [1, 2, 3]
            ext_rot   += [noop, noop, noop]
        else:
            ext_faces += [5, 2, 4]
            ext_rot   += [noop, cpt.u_turn, noop]

    for ef, er in zip(ext_faces, ext_rot):
        f_rot = er(faces[ef].rot)
        faces[ef].absorp += GRID_SIZE * i.param
        for y in (range(GRID_SIZE) if i.scope == Scope.COL else [i.scope_val - 1]):
            for x in (range(GRID_SIZE) if i.scope == Scope.ROW else [i.scope_val - 1]):
                match f_rot:
                    case cpt.RIGHT:
                        aloc = (x, y)
                    case cpt.LEFT:
                        aloc = (GRID_SIZE - 1 - x, GRID_SIZE - 1 - y)
                    case cpt.DOWN:
                        aloc = (y, GRID_SIZE - 1 - x)
                    case cpt.UP:
                        aloc = (GRID_SIZE - 1 - y, x)
                nodes[ef][aloc] = (nodes[ef][aloc] + i.param) % 100

def apply_rot(nodes, faces, r):
    match r:
        case None:
            return
        case 'L':
            permu = [4, 1, 5, 3, 2, 0]
            rotfn = [noop, cpt.right_turn, cpt.u_turn, cpt.left_turn, cpt.u_turn, noop]
        case 'R':
            permu = [5, 1, 4, 3, 0, 2]
            rotfn = [noop, cpt.left_turn, cpt.u_turn, cpt.right_turn, noop, cpt.u_turn]
        case 'D':
            permu = [1, 2, 3, 0, 4, 5]
            rotfn = [noop, noop, noop, noop, cpt.left_turn, cpt.right_turn]
        case 'U':
            permu = [3, 0, 1, 2, 4, 5]
            rotfn = [noop, noop, noop, noop, cpt.right_turn, cpt.left_turn]

    new_nodes = [nodes[p] for p in permu]
    new_faces = [faces[p] for p in permu]
    for o in range(6):
        nodes[o] = new_nodes[o]
        faces[o] = new_faces[o]
        faces[o].rot = rotfn[o](faces[o].rot)

def part1(output=False):
    insts, rots = parse()
    nodes = blank_grid()
    faces = {n: Face() for n in nodes}
    for i, r in zip_longest(insts, rots):
        apply_inst(nodes, faces, i)
        apply_rot(nodes, faces, r)
    face_absorps = sorted((f.absorp for f in faces.values()), reverse=True)
    return big_pi(face_absorps[:2])

def dom_sum(nodes, f):
    rows = [sum(nodes[f][(x, y)] + 1 for x in range(GRID_SIZE)) for y in range(GRID_SIZE)]
    cols = [sum(nodes[f][(x, y)] + 1 for y in range(GRID_SIZE)) for x in range(GRID_SIZE)]
    return max(rows + cols)

def part2(output=False):
    insts, rots = parse()
    nodes = blank_grid()
    faces = {n: Face() for n in nodes}
    for i, r in zip_longest(insts, rots):
        apply_inst(nodes, faces, i)
        apply_rot(nodes, faces, r)
    face_doms = (dom_sum(nodes, f) for f in faces)
    return big_pi(face_doms)

def part3(output=False):
    insts, rots = parse()
    nodes = blank_grid()
    faces = {n: Face() for n in nodes}
    for i, r in zip_longest(insts, rots):
        apply_inst(nodes, faces, i, True)
        apply_rot(nodes, faces, r)
    face_doms = (dom_sum(nodes, f) for f in faces)
    return big_pi(face_doms)

if __name__ == '__main__':
    print('Part 1:', part1(True))
    print('Part 2:', part2(True))
    print('Part 3:', part3(True))
