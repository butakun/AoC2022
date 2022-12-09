import numpy as np


def move_tail(H, T):
    dx, dy = H[0] - T[0], H[1] - T[1]
    if abs(dx) <= 1 and abs(dy) <= 1:
        return np.array([0, 0])
    if dx == 0:
        return np.array([0, int(dy / abs(dy))])
    if dy == 0:
        return np.array([int(dx / abs(dx)), 0])
    return np.array([int(dx / abs(dx)), int(dy / abs(dy))])


def step(direction):
    if direction == "U":
        dH = 0, -1
    elif direction == "D":
        dH = 0, 1
    elif direction == "L":
        dH = -1, 0
    elif direction == "R":
        dH = 1, 0
    else:
        raise ValueError(f"{move}")
    return np.array(dH)


def main(filename):
    moves = [ l.strip().split() for l in open(filename) ]
    moves = [ [m[0], int(m[1])] for m in moves ]

    HH = [np.array([0, 0]) for _ in range(10)]
    visited = set([tuple(HH[9])])

    for direction, steps in moves:

        dH = step(direction)
        for istep in range(steps):
            HH[0] += dH
            for H, h in zip(HH[:-1], HH[1:]):
                dh = move_tail(H, h)
                h += dh
            visited.add(tuple(HH[9]))
            print("HH", [H.tolist() for H in HH])

    print(visited)
    print(len(visited))

if __name__ == "__main__":
    import sys
    main(sys.argv[1])
