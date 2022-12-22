import numpy as np
import re


class Grid(object):
    def __init__(self, grid, imins, imaxs, jmins, jmaxs):
        self.grid = grid
        self.imins = imins
        self.imaxs = imaxs
        self.jmins = jmins
        self.jmaxs = jmaxs

    def one_step(self, ij, dij):
        i, j = ij
        # no diagonal dij
        ij1 = ij + dij
        i1, j1 = ij1
        if ij1[0] < self.imins[j1]:
            ij1[0] = imaxs[j1]
        elif ij1[0] > self.imaxs[j1]:
            ij1[0] = imins[j1]
        elif ij1[1] < self.imins[j1]:
            ij1[1] = imaxs[j1]
        elif ij1[1] > self.imaxs[j1]:
            ij1[1] = imins[j1]
        return ij1


def read(filename):
    with open(filename) as f:
        lines = f.read().splitlines()

    # grid[x, y] = grid[i, j]
    idim = max([ len(l) for l in lines[:-2] ])
    jdim = len(lines) - 2
    inst = lines[-1]

    ops = []
    token = ""
    for c in inst:
        if c.isdigit():
            token += c
        elif c == "R" or c == "L":
            ops.append(int(token))
            ops.append(c)
            token = ""

    grid = np.zeros((idim, jdim), np.uint8)
    for j, line in enumerate(lines[:-2]):
        for i, c in enumerate(line):
            grid[i, j] = 0 if c == "." else 1 if c == "#" else 2
        grid[len(line):, j] = 2

    istart = 0
    jstart = np.where(grid[istart, :] == 0)[0][0]

    direc = "R"

    imins = np.zeros((jdim), np.uint8)
    imaxs = np.zeros((jdim), np.uint8)
    jmins = np.zeros((idim), np.uint8)
    jmaxs = np.zeros((idim), np.uint8)
    for j in range(jdim):
        ends = np.where(grid[:, j] != 2)[0]
        if len(ends) > 0:
            imins[j] = ends[0]
            imaxs[j] = ends[-1]
        else:
            imins[j] = 0 
            imaxs[j] = 0
    for i in range(idim):
        ends = np.where(grid[i, :] != 2)[0]
        if len(ends) > 0:
            jmins[i] = ends[0]
            jmaxs[i] = ends[-1]
        else:
            jmins[i] = 0
            jmaxs[i] = 0

    print(grid.T)
    print(ops)
    print(imins, imaxs)
    print(jmins, jmaxs)
    print(istart, jstart)

    G = Grid(grid, imins, imaxs, jmins, jmaxs)
    return G, ops, np.array([istart, jstart]), direc


def one_op(G, ij, direc, op):
    if op == "L":
        if direc == "R":
            direc = "U"
        elif direc == "U":
            direc = "L"
        elif direc == "L":
            direc = "D"
        elif direc == "D":
            direc = "R"
    elif op == "R":
        if direc == "R":
            direct = "D"
        elif direc == "U":
            direc = "R"
        elif direc == "L":
            direc = "U"
        elif direc == "D":
            direc = "L"
    else:
        if direc == "R":
            dij = np.array([1, 0], np.uint8)
        elif direc == "U":
            dij = np.array([0, -1], np.uint8)
        elif direc == "L":
            dij = np.array([-1, 0], np.uint8)
        elif direc == "D":
            dij = np.array([0, 1], np.uint8)
        else:
            raise ValueError(direc)

        ijnext = ij.copy()
        for step in range(op):
            ij_ = G.one_step(ijnext, dij)
            c_ = G.grid[ij_[0], ij_[1]] 
            print("ij_, c = ", ij_, c_)
            if c_ == 0:
                ijnext = ij_
            elif c_ == 1:
                break

        ij = ijnext
    return ij


def main(filename):
    G, ops, ij0, direc = read(filename)

    ij = ij0
    for op in ops:
        ij = one_op(G, ij, direc, op)
        print(op, ij)


if __name__ == "__main__":
    import sys
    main(sys.argv[1])
