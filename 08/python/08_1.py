import numpy as np

def visible(g, jdim):

    # from left
    vl = np.zeros_like(g, bool)
    hmax = -1
    for j in range(jdim):
        if g[j] > hmax:
            hmax = g[j]
            vl[j] = True

    # from right
    vr = np.zeros_like(g, bool)
    hmax = -1
    for j in range(jdim - 1, -1, -1):
        if g[j] > hmax:
            hmax = g[j]
            vr[j] = True

    return vl | vr


def main(filename):
    with open(filename) as f:
        G = np.array([ [int(c) for c in line.strip()] for line in f ])

    print(G)

    Vlr = np.zeros_like(G, dtype=bool)
    Vtb = np.zeros_like(G, dtype=bool)

    idim, jdim = G.shape
    for i in range(idim):
        vlr = visible(G[i, :], jdim)
        Vlr[i, :] = vlr

    for j in range(jdim):
        vtb = visible(G[:, j], idim)
        Vtb[:, j] = vtb

    print("from left right")
    print(Vlr)
    print("from top bottom")
    print(Vtb)
    print("from all dirs")
    V = Vlr | Vtb
    print(V)
    print(V.sum())


if __name__ == "__main__":
    import sys
    main(sys.argv[1])
