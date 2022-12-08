import numpy as np

def main(filename):
    with open(filename) as f:
        G = np.array([ [int(c) for c in line.strip()] for line in f ])

    print(G)

    Vl = np.zeros_like(G, dtype=bool)
    Vr = np.zeros_like(G, dtype=bool)
    Vt = np.zeros_like(G, dtype=bool)
    Vb = np.zeros_like(G, dtype=bool)

    idim, jdim = G.shape
    for i in range(idim):
        print("i = ", i)
        dx = G[i, 1:] - G[i, :-1]

        left = np.where((dx[1:] - dx[:-1]) > 0)[0]
        print("left = ", left)
        Vl[i, 1:][left] = True
        Vl[i, 0] = True
        print(Vl)
        d = np.where(Vl[i, :] == False)[0]
        print(d)
        if len(d) > 0:
            Vl[i, d[0]:] = False
        break

    print("from left")
    print(Vl)

    return
    print("from right")
    print(Vr)
    print("from top")
    print(Vt)
    print("from bottom")
    print(Vb)

if __name__ == "__main__":
    import sys
    main(sys.argv[1])
