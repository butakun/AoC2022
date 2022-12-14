import numpy as np
from collections import deque


class Cave(object):
    def __init__(self, grid, pmin, pmax):
        self.grid = grid
        self.pmin = pmin
        self.pmax = pmax

    def at(self, x, y):
        ii = x - self.pmin[0]
        jj = y - self.pmin[1]
        sh = self.grid.shape
        if ii < 0 or jj < 0 or ii >= sh[0] or jj >= sh[1]:
            return 0
        return self.grid[ii, jj]

    def set(self, x, y, v):
        ii = x - self.pmin[0]
        jj = y - self.pmin[1]
        sh = self.grid.shape
        assert ii >= 0 and jj >= 0 and ii < sh[0] and jj < sh[1]
        self.grid[ii, jj] = v

    def isinside(self, x, y):
        ii = x - self.pmin[0]
        jj = y - self.pmin[1]
        sh = self.grid.shape
        return ii >= 0 and jj >= 0 and ii < sh[0] and jj < sh[1]

    def xy_to_ij(self, x, y):
        ii = x - self.pmin[0]
        jj = y - self.pmin[1]
        return ii, jj

    def ij_to_xy(self, i, j):
        x = self.pmin[0] + i
        y = self.pmin[1] + j
        return x, y

    def at_ij(self, i, j):
        sh = self.grid.shape
        assert i >= 0 and j >= 0 and i < sh[0] and j < sh[1]
        return self.grid[i, j]

    def __repr__(self):
        buf = "\n".join(
            ["".join([(lambda c: "." if c == 0 else "#" if c == 1 else "*")(c) for c in l]) for l in self.grid.T]
            )
        return buf


def read(filename):
    with open(filename) as f:
        lines = [ [ [int(xy) for xy in p.split(",")] for p in l.split("->") ] for l in f ]

    bbs = []
    for l in lines:
        pp = np.array(l)
        pmin = pp.min(axis=0)
        pmax = pp.max(axis=0)
        bb = [pmin, pmax]
        bbs.append(bb)
    bbs = np.array(bbs)

    xmin = bbs[:, :, 0].flatten().min()
    xmax = bbs[:, :, 0].flatten().max()
    ymin = bbs[:, :, 1].flatten().min()
    ymin = 0
    ymax = bbs[:, :, 1].flatten().max()
    ymax = ymax + 2

    xmin = 500 - ymax
    xmax = 500 + ymax

    lines.append([[xmin, ymax], [xmax, ymax]])

    idim = xmax - xmin + 1
    jdim = ymax - ymin + 1
    print(xmin, xmax)
    print(ymin, ymax)
    print(idim, jdim)

    grid = np.zeros((idim, jdim), np.uint8)
    pmin = [xmin, ymin]
    pmax = [xmax, ymax]

    for l in lines:
        for p1, p2 in zip(l[:-1], l[1:]):
            ij1 = np.array(p1) - pmin
            ij2 = np.array(p2) - pmin
            print("line: ", p1, p2, ij1, ij2)
            dij = ij2 - ij1
            if dij[0] == 0:
                i = ij1[0]
                j1 = min(ij1[1], ij2[1])
                j2 = max(ij1[1], ij2[1])
                grid[i, j1:j2+1] = 1
            elif dij[1] == 0:
                j = ij1[1]
                i1 = min(ij1[0], ij2[0])
                i2 = max(ij1[0], ij2[0])
                grid[i1:i2+1, j] = 1
            else:
                raise ValueError(f"{dij}")
    return Cave(grid, pmin, pmax)


"""
def drop_sand(cave):
    q = deque([[500, 0]])

    iloop = 0
    while q:
        x, y = q.popleft()
        for xc, yc in [[x, y+1], [x-1, y+1], [x+1, y+1]]:
            if cave.isinside(xc, yc) and cave.at(xc, yc) == 0:
                q.append([xc, yc])
        if cave.at(x, y) != 0:
            continue

        i, j = cave.xy_to_ij(x, y)
        j2 = np.where(cave.grid[i, j:] > 0)[0][0] + j
        cave.grid[i, j:j2] = 2
        
        x2, y2 = cave.ij_to_xy(i, j2-1)
        print(f"filled {x, y} - {x2, y2}")

        iloop += 1
"""


def step(cave, sands, isand):
    if isand >= len(sands):
        # release new sand unit
        if cave.at(500, 0) != 0:
            return "NOMORE"
        sands.append([500, 0])
        cave.set(500, 0, 2)
        return "OK"

    psand = sands[isand]
    psx, psy = psand
    if cave.at(psx, psy + 1) == 0:
        if not cave.isinside(psx, psy+1):
            return "NOMORE"
        cave.set(psx, psy, 0)
        cave.set(psx, psy + 1, 2)
        psand[1] = psy + 1
        return "OK"
    elif cave.at(psx-1, psy+1) == 0:
        if not cave.isinside(psx-1, psy+1):
            return "NOMORE"
        cave.set(psx, psy, 0)
        cave.set(psx-1, psy+1, 2)
        psand[0] = psx-1
        psand[1] = psy+1
        return "OK"
    elif cave.at(psx+1, psy+1) == 0:
        if not cave.isinside(psx+1, psy+1):
            return "NOMORE"
        cave.set(psx, psy, 0)
        cave.set(psx+1, psy+1, 2)
        psand[0] = psx+1
        psand[1] = psy+1
        return "OK"

    return "STUCK"


def main(filename):
    cave = read(filename)
    print(cave)

    sands = []
    isand = 0
    ilastsand = -1
    i = 0
    while True:
        ok = step(cave, sands, isand)
        if ok == "NOMORE":
            break
        if ok == "STUCK":
            ilastsand = isand
            isand += 1
        if i % 10000 == 0:
            print(f"{i}: {isand}")
        i += 1


    print(cave)
    print("last id = ", ilastsand)
    print("haw many = ", ilastsand + 1)

if __name__ == "__main__":
    import sys
    main(sys.argv[1])
