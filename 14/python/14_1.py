import numpy as np


class Cave(object):
    def __init__(self, grid, pmin, pmax):
        self.grid = grid
        self.pmin = pmin
        self.pmax = pmax

    def at(self, i, j):
        ii = i - self.pmin[0]
        jj = j - self.pmin[1]
        sh = self.grid.shape
        if ii < 0 or jj < 0 or ii >= sh[0] or jj >= sh[1]:
            return 0
        return self.grid[ii, jj]

    def set(self, i, j, v):
        ii = i - self.pmin[0]
        jj = j - self.pmin[1]
        sh = self.grid.shape
        assert ii >= 0 and jj >= 0 and ii < sh[0] and jj < sh[1]
        self.grid[ii, jj] = v

    def isinside(self, i, j):
        ii = i - self.pmin[0]
        jj = j - self.pmin[1]
        sh = self.grid.shape
        return ii >= 0 and jj >= 0 and ii < sh[0] and jj < sh[1]

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


def step(cave, sands, isand):
    if isand >= len(sands):
        # release new sand unit
        if cave.at(500, 1) != 0:
            return "NOMORE"
        sands.append([500, 0])

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
    print(cave.grid.T)

    sands = []
    isand = 0
    ilastsand = -1
    for i in range(100000):
        print(f"Step {i}: isand = {isand}")
        ok = step(cave, sands, isand)
        if ok == "NOMORE":
            break
        #print(cave.grid.T)
        if ok == "STUCK":
            ilastsand = isand
            isand += 1

    print("last id = ", ilastsand)
    print("haw many = ", ilastsand + 1)

if __name__ == "__main__":
    import sys
    main(sys.argv[1])
