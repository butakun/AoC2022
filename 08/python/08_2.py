import numpy as np

def view(g, jdim):
    vr = np.zeros_like(g)
    vl = np.zeros_like(g)

    for j in range(jdim):
        cansee = 0
        for jj in range(j+1, jdim):
            if True or g[jj] <= g[j]:
                cansee += 1
            if g[jj] >= g[j]:
                break
        vr[j] = cansee

    for j in range(jdim):
        cansee = 0
        for jj in range(j-1, -1, -1):
            if True or g[jj] <= g[j]:
                cansee += 1
            if g[jj] >= g[j]:
                break
        vl[j] = cansee
    return vr, vl


def main(filename):
    with open(filename) as f:
        G = np.array([ [int(c) for c in line.strip()] for line in f ])

    print(G)

    idim, jdim = G.shape

    Vr = np.zeros_like(G)
    Vl = np.zeros_like(G)
    Vd = np.zeros_like(G)
    Vu = np.zeros_like(G)

    for i in range(idim):
        vr, vl = view(G[i, :], jdim)
        Vr[i, :] = vr
        Vl[i, :] = vl

    for j in range(jdim):
        vd, vu = view(G[:, j], idim)
        Vd[:, j] = vd
        Vu[:, j] = vu

    print("can see right")
    print(Vr)
    print("can see left")
    print(Vl)
    print("can see down")
    print(Vd)
    print("can see up")
    print(Vu)

    V = Vr * Vl * Vd * Vu
    print(V)
    print(V.max())


if __name__ == "__main__":
    import sys
    main(sys.argv[1])
