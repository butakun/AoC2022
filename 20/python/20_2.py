import sys
import numpy as np


def main(filename):
    multiply = 811589153
    V = [int(v) * multiply for v in open(filename).read().splitlines()]
    N = len(V)
    VP = [ i for i in range(len(V)) ]
    VP0 = VP.copy()

    debug = N < 10

    for mix in range(10):
        for vp0 in VP0:
            vpp_old = VP.index(vp0)
            vpp_new = (vpp_old + V[vp0]) % (N - 1)
            vpp = VP.pop(vpp_old)
            VP.insert(vpp_new, vpp)
            if debug:
                print(f"{V[vp0]} moved : {[V[i] for i in VP]}, VP = {VP}")

    VV = [ V[i] for i in VP ]
    i_0 = VV.index(0)
    i1000 = (i_0 + 1000) % N
    i2000 = (i_0 + 2000) % N
    i3000 = (i_0 + 3000) % N
    print(i1000)
    print(i2000)
    print(i3000)
    print(VV[i1000])
    print(VV[i2000])
    print(VV[i3000])
    print(VV[i1000] + VV[i2000] + VV[i3000])


if __name__ == "__main__":
    import sys
    main(sys.argv[1])
