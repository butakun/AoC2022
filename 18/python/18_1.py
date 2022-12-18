import numpy as np


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

    S = 0
    for x, y, z in pts:
        xp = x + 1
        yp = y + 1
        zp = z + 1
        S += 1 if V[xp-1, yp  , zp  ] == 0 else 0
        S += 1 if V[xp+1, yp  , zp  ] == 0 else 0
        S += 1 if V[xp  , yp-1, zp  ] == 0 else 0
        S += 1 if V[xp  , yp+1, zp  ] == 0 else 0
        S += 1 if V[xp  , yp  , zp-1] == 0 else 0
        S += 1 if V[xp  , yp  , zp+1] == 0 else 0

    print(S)

if __name__ == "__main__":
    import sys
    main(sys.argv[1])
