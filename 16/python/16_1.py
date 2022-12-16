from collections import defaultdict


class ActionGraph(object):
    def __init__(self, network, Qgas):
        self.network = network
        self.Qgas = Qgas

    def __getitem__(self, u):
        actions = []
        for v in self.network[u]:
            if self.Qgas[u] > 0:
                actions.append((u, True))
            actions.append((v, True))


def evaluate_Qtotal(path, network, Qgas):
    assert(len(path) == 30)


def read(filename):
    def readline(line):
        tokens = line.strip().split()
        u = tokens[1]
        q = int(tokens[4].split("=")[1][:-1])
        vv = [ t.rstrip(",") for t in tokens[9:] ]
        return u, q, vv
    with open(filename) as f:
        lines = [ readline(line) for line in f ]

    G = defaultdict(list)
    Qgas = {}
    for u, q, vv in lines:
        G[u] = vv
        Qgas[u] = q

    return G, Qgas


def main(filename):
    G, Qgas = read(filename)
    print(G, Qgas)

    open_valves = dict()
    u = "AA"
    q = [(u, False)]
    came_from = []
    t = 0
    while q:
        u, valve = q.pop()
        if Qgas[u] > 0:
            q.append((u, True))
        for v in G[u]:
            q.append((v, False))

if __name__ == "__main__":
    import sys
    main(sys.argv[1])
