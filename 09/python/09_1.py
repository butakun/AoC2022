import numpy as np


def move_tail(H, T):
    dx, dy = H[0] - T[0], H[1] - T[1]
    if abs(dx) <= 1 and abs(dy) <= 1:
        return 0, 0
    if dx == 0:
        return 0, int(dy / abs(dy))
    if dy == 0:
        return int(dx / abs(dx)), 0
    return int(dx / abs(dx)), int(dy / abs(dy))


def main(filename):
    moves = [ l.strip().split() for l in open(filename) ]
    moves = [ [m[0], int(m[1])] for m in moves ]

    print(moves)

    H = [0, 0]
    T = [0, 0]
    visited = set([tuple(T)])

    for direction, steps in moves:
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

        for step in range(steps):
            H[0] += dH[0]
            H[1] += dH[1]
            dT = move_tail(H, T)
            T[0] += dT[0]
            T[1] += dT[1]
            visited.add(tuple(T))
            print("H, dT, T", H, dT, T)

    print(visited)
    print(len(visited))

if __name__ == "__main__":
    import sys
    main(sys.argv[1])
