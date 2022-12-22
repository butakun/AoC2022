import numpy as np
import logging

logging.basicConfig(level=logging.INFO)

class Grid(object):
    def __init__(self, grid, imins, imaxs, jmins, jmaxs):
        self.grid = grid
        self.imins = imins
        self.imaxs = imaxs
        self.jmins = jmins
        self.jmaxs = jmaxs

        idim, jdim = self.grid.shape
        self.fdim = max(idim, jdim) // 4
        self.fidim = idim // self.fdim
        self.fjdim = jdim // self.fdim

        self.patch_faces_together()

    def patch_faces_together(self):
        idim, jdim = self.grid.shape
        print("fidim, fjdim = ", self.fidim, self.fjdim)
        #faces = np.zeros((self.fidim, self.fjdim, 2), np.int32)
        #faces[:, :, :] = -1
        faces = {}
        #bases = np.zeros((self.fidim, self.fjdim, 2, 2), np.int32)
        bases = {}

        if self.fdim == 4:
            faces[( 0,  0)] = (2, 0)
            faces[( 1,  0)] = (2, 0)
            faces[( 3,  0)] = (3, 2)
            faces[( 3,  1)] = (3, 2)
            faces[( 0,  2)] = (2, 2)
            faces[( 1,  2)] = (2, 2)
            faces[(-1,  1)] = (3, 2)
            faces[( 2, -1)] = (0, 1)
            faces[( 4,  2)] = (2, 0)
            faces[( 3,  3)] = (0, 1)
            faces[( 2,  3)] = (0, 1)
            bases[( 0,  0)] = np.array([[-1,  0], [ 0, -1]], np.int32)
            bases[( 1,  0)] = np.array([[ 0, -1], [ 1,  0]], np.int32)
            bases[( 3,  0)] = np.array([[-1,  0], [ 0, -1]], np.int32)
            bases[( 3,  1)] = np.array([[ 0, -1], [ 1,  0]], np.int32)
            bases[( 0,  2)] = np.array([[ 1,  0], [ 0, -1]], np.int32)
            bases[( 1,  2)] = np.array([[ 0, -1], [ 1,  0]], np.int32)
            bases[(-1,  1)] = np.array([[ 0,  1], [-1,  0]], np.int32)
            bases[( 2, -1)] = np.array([[-1,  0], [ 0, -1]], np.int32)
            bases[( 4,  2)] = np.array([[-1,  0], [ 0, -1]], np.int32)
            bases[( 3,  3)] = np.array([[ 0, -1], [ 1,  0]], np.int32)
            bases[( 2,  3)] = np.array([[-1,  0], [ 0, -1]], np.int32)
        elif self.fdim == 50:
            # faces[ghost_face] = {from_face_1: to_face_1, from_face_2: to_face_2}
            faces[( 1, -1)] = {(1, 0): (0, 3)}
            faces[( 2, -1)] = {(2, 0): (0, 3)}
            faces[( 0,  0)] = {(1, 0): (0, 2)}
            faces[( 3,  0)] = {(2, 0): (1, 2)}
            faces[( 0,  1)] = {(1, 1): (0, 2), (0, 2): (1, 1)}
            faces[( 2,  1)] = {(1, 1): (2, 0), (2, 0): (1, 1)}
            faces[(-1,  2)] = {(0, 2): (1, 0)}
            faces[( 2,  2)] = {(1, 2): (2, 0)}
            faces[(-1,  3)] = {(0, 3): (1, 0)}
            faces[( 1,  3)] = {(0, 3): (1, 2), (1, 2): (0, 3)}
            faces[( 0,  4)] = {(0, 3): (2, 0)}
            bases[( 1, -1)] = {(1, 0): [[ 0, -1], [ 1,  0]]}
            bases[( 2, -1)] = {(2, 0): [[ 1,  0], [ 0,  1]]}
            bases[( 0,  0)] = {(1, 0): [[-1,  0], [ 0, -1]]}
            bases[( 3,  0)] = {(2, 0): [[-1,  0], [ 0, -1]]}
            bases[( 0,  1)] = {(1, 1): [[ 0,  1], [-1,  0]], (0, 2): [[0, -1], [1, 0]]}
            bases[( 2,  1)] = {(1, 1): [[ 0,  1], [-1,  0]], (2, 0): [[0, -1], [1, 0]]}
            bases[(-1,  2)] = {(0, 2): [[-1,  0], [ 0, -1]]}
            bases[( 2,  2)] = {(1, 2): [[-1,  0], [ 0, -1]]}
            bases[(-1,  3)] = {(0, 3): [[ 0,  1], [-1,  0]]}
            bases[( 1,  3)] = {(0, 3): [[ 0,  1], [-1,  0]], (1, 2): [[0, -1], [1, 0]]}
            bases[( 0,  4)] = {(0, 3): [[ 1,  0], [ 0,  1]]}
            for kghost, v in bases.items():
                vnew = {kfrom: np.array(T, np.int32) for kfrom, T in v.items()}
                v.update(vnew)
        else:
            raise NotImplementedError

        self.faces = faces
        self.bases = bases

    def is_on_ghost_face(self, i, j):
        fi = i // self.fdim
        fj = j // self.fdim
        return (fi, fj) in self.faces

    def translate_to_real_face(self, ij0, ij1, dij1=None):
        i0, j0 = ij0
        fi0 = i0 // self.fdim
        fj0 = j0 // self.fdim
        face_from = (fi0, fj0)

        i1, j1 = ij1
        fi1 = i1 // self.fdim
        fj1 = j1 // self.fdim
        logging.info(f"ij {ij1} is in face ({fi1}, {fj1})")
        if (fi1, fj1) not in self.faces:
            if dij1 is not None:
                return ij1, dij1
            else:
                return ij1

        i1_0, j1_0 = self.fdim * fi1, self.fdim * fj1
        ij1_origin = np.array([i1_0, j1_0], np.int32)
        ij1_ = ij1 - ij1_origin
        print(f"ij1, ij1_origin, ij1_ = {ij1}, {ij1_origin}, {ij1_}")
        T = self.bases[(fi1, fj1)][face_from]
        ij2_ = np.dot(T, ij1_)  # ij2_ can still contain negative indices
        print(f"ij2_ = {ij2_}")

        fi2, fj2 = self.faces[(fi1, fj1)][face_from]
        i2_0, j2_0 = self.fdim * fi2, self.fdim * fj2
        i2_1, j2_1 = i2_0 + self.fdim - 1, j2_0 + self.fdim - 1

        ij2_origin = np.zeros_like(ij1)
        if T[0, 0] == 1:
            ij2_origin[0] = i2_0
        elif T[0, 0] == -1:
            ij2_origin[0] = i2_1
        elif T[0, 1] == 1:
            ij2_origin[0] = i2_0
        elif T[0, 1] == -1:
            ij2_origin[0] = i2_1
        if T[1, 0] == 1:
            ij2_origin[1] = j2_0
        elif T[1, 0] == -1:
            ij2_origin[1] = j2_1
        elif T[1, 1] == 1:
            ij2_origin[1] = j2_0
        elif T[1, 1] == -1:
            ij2_origin[1] = j2_1

        ij2 = ij2_origin + ij2_

        if dij1 is not None:
            dij2 = np.dot(T, dij1)
            return ij2, dij2
        else:
            return ij2

    def one_step(self, ij, dij):
        i, j = ij
        # no diagonal dij
        ij1 = ij + dij
        ij1, dij1 = self.translate_to_real_face(ij, ij1, dij)
        i1, j1 = ij1

        if self.grid[ij1[0], ij1[1]] == 0:
            ij = ij1
            dij = dij1
        else:
            logging.info("but can't move there so staying put at {ij} with dij {dij}")
        return ij, dij

    def go_around(self, ij1, ij2, dij1):
        raise NotImplementedError

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


def dij_to_direc(dij):
    if dij.tolist() == [1, 0]:
        return "R"
    elif dij.tolist() == [-1, 0]:
        return "L"
    elif dij.tolist() == [0, 1]:
        return "D"
    elif dij.tolist() == [0, -1]:
        return "U"

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
            ijnext, dij = G.one_step(ijnext, dij)
            logging.info(f"ijnext = {ijnext}, dij = {dij}")

        ij = ijnext
        direc = dij_to_direc(dij)
    return ij, direc


def main(filename):
    G, ops, ij0, direc = read(filename)

    logging.info(f"fdim = {G.fdim}")


    path = [(ij0, direc)]
    ij = ij0
    for op in ops:
        logging.info(f"at {ij} direc {direc}, executing op = {op}")
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
