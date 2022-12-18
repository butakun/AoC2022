import numpy as np
from collections import deque


class Voxels(object):
    def __init__(self, voxels):
        self.V = voxels

    def __getitem__(self, i):
        x, y, z = i
        neighbors = []
        occupied = []
        for x2, y2, z2 in [[x,y,z-1],[x,y,z+1],[x,y-1,z],[x,y+1,z],[x-1,y,z],[x+1,y,z]]:
            if x2 < 0 or x2 >= self.V.shape[0]:
                continue
            if y2 < 0 or y2 >= self.V.shape[1]:
                continue
            if z2 < 0 or z2 >= self.V.shape[2]:
                continue
            if self.V[x2, y2, z2] == 0:
                neighbors.append((x2, y2, z2))
        return neighbors


def connected_component(G, start, debug=0):
    visited = set([start])
    occupied = set()
    Q = deque([start])
    while Q:
        u = Q.popleft()
        for v in G[u]:
            if v not in visited:
                Q.append(v)
                visited.add(v)
    return set(visited)


def read(filename):
    with open(filename) as f:
        pts = np.array([ [int(v) for v in l.strip().split(",") ] for l in f ])
    return pts


def main(filename):
    pts = read(filename)

    xx = sorted([p[0] for p in pts])
    yy = sorted([p[1] for p in pts])
    zz = sorted([p[2] for p in pts])
    print("xx = ", xx)
    print("yy = ", yy)
    print("zz = ", zz)

    xmax = max(xx)
    ymax = max(yy)
    zmax = max(zz)

    V = np.zeros((xmax+3, ymax+3, zmax+3), np.uint8)
    for x, y, z in pts:
        V[x+1, y+1, z+1] = 1

    voxels = Voxels(V)
    outside = connected_component(voxels, (0, 0, 0))
    print(len(outside))
    for x, y, z in outside:
        V[x, y, z] = 2

    S = 0
    for x, y, z in pts:
        xp = x + 1
        yp = y + 1
        zp = z + 1
        S += 1 if V[xp-1, yp  , zp  ] == 2 else 0
        S += 1 if V[xp+1, yp  , zp  ] == 2 else 0
        S += 1 if V[xp  , yp-1, zp  ] == 2 else 0
        S += 1 if V[xp  , yp+1, zp  ] == 2 else 0
        S += 1 if V[xp  , yp  , zp-1] == 2 else 0
        S += 1 if V[xp  , yp  , zp+1] == 2 else 0

    print(S)

if __name__ == "__main__":
    import sys
    main(sys.argv[1])
