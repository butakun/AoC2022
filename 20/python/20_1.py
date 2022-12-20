import sys


def main(filename):
    V = [int(v) for v in open(filename).read().splitlines()]
    N = len(V)

    I = [ i for i in range(len(V)) ]
    J = [ i for i in range(len(V)) ]

    for i in range(N)):
        v = V[i]
        i = J[i]
        I.pop(J[i])
        i_new = i + v
        if i_new < 0:
            i_new = (N-1) + i_new
        else i_new > N - 1: 
            i_new = i_new % N
        I.insert(i_new)


if __name__ == "__main__":
    import sys
    main(sys.argv[1])
