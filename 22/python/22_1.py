import numpy as np
import logging


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
        if dij[0] != 0 and dij[1] == 0:
            if ij1[0] < self.imins[ij1[1]]:
                ij1[0] = self.imaxs[ij1[1]]
                logging.info(f"hit wall to left, ij1 wrap around to {ij1}")
            elif ij1[0] > self.imaxs[ij1[1]]:
                ij1[0] = self.imins[ij1[1]]
                logging.info("hit wall to right, ij1 wrap around to {ij1}")
        elif dij[0] == 0 and dij[1] != 0:
            if ij1[1] < self.jmins[ij1[0]]:
                ij1[1] = self.jmaxs[ij1[0]]
                logging.info("hit wall up, ij1 wrap around to {ij1}")
            elif ij1[1] > self.jmaxs[ij1[0]]:
                ij1[1] = self.jmins[ij1[0]]
                logging.info("hit wall down, ij1 wrap around to {ij1}")
        else:
            raise ValueError(f"dij diagonal {dij}")

        if self.grid[ij1[0], ij1[1]] == 0:
            ij = ij1
        else:
            logging.info("but can't move there so staying put at {ij}")
        return ij

    def prettified(self, path=None):
        direc_to_char = { "R": ">", "U": "^", "L": "<", "D": "v" }
        chars = { 0: ".", 1: "#", 2: " " }
        buf = [ [ chars[c] for c in line ] for line in self.grid.T ]
        if path:
            for (i, j), direc in path:
                buf[j][i] = direc_to_char[direc]

        buf = "\n".join([ "".join([c for c in line]) for line in buf ])

        return buf


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
    if token:
        if token.isdigit():
            ops.append(int(token))
        else:
            assert token == "L" or token == "R"
            ops.append(token)

    grid = np.zeros((idim, jdim), np.uint8)
    for j, line in enumerate(lines[:-2]):
        for i, c in enumerate(line):
            grid[i, j] = 0 if c == "." else 1 if c == "#" else 2
        grid[len(line):, j] = 2

    jstart = 0
    istart = np.where(grid[:, jstart] == 0)[0][0]

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
            direc = "D"
        elif direc == "U":
            direc = "R"
        elif direc == "L":
            direc = "U"
        elif direc == "D":
            direc = "L"
    else:
        if direc == "R":
            dij = np.array([1, 0], np.int32)
        elif direc == "U":
            dij = np.array([0, -1], np.int32)
        elif direc == "L":
            dij = np.array([-1, 0], np.int32)
        elif direc == "D":
            dij = np.array([0, 1], np.int32)
        else:
            raise ValueError(direc)

        ijnext = ij.copy()
        for step in range(op):
            ijnext = G.one_step(ijnext, dij)

        ij = ijnext
    return ij, direc


def main(filename):
    G, ops, ij0, direc = read(filename)

    print(G.prettified())

    path = [(ij0, direc)]
    ij = ij0
    for op in ops:
        ij, direc = one_op(G, ij, direc, op)
        path.append((ij, direc))
        print(op, ij, direc)

    print(G.prettified(path))

    direc_to_digit = { "R": 0, "D": 1, "L": 2, "U": 3 }
    password = 1000 * (ij[1] + 1) + 4 * (ij[0] + 1) + direc_to_digit[direc]
    print(password)


if __name__ == "__main__":
    import sys
    main(sys.argv[1])
