from dijkstra import dijkstra, dijkstra2
from collections import defaultdict
from itertools import product, permutations


class ActionNode(object):
    def __init__(self, path_1, path_2):
        self.path_1 = path_1
        self.path_2 = path_2
        self.t_1 = None
        self.t_2 = None
        self.q_1 = None
        self.q_2 = None

    def __hash__(self):
        return hash((tuple(self.path_1), tuple(self.path_2)))

    def __repr__(self):
        return f"{self.path_1[-1]}, {self.path_2[-1]}"


class ActionGraph(object):
    """ u = (room, time_remaining, valves) """
    def __init__(self, network, Qgas, time_start):
        self.network = network
        self.good_valves = [ k for k, v in Qgas.items() if v > 0 ]
        self.Qgas = Qgas
        self.valves = [ k for k in Qgas.keys() ]
        self.time_start = time_start
        self.cached_time = dict()

    def next_actions(self, u, cost, cost_min):
        actions = []

        opened = set(u.path_1 + u.path_2)
        still_closed = [ v for v in self.good_valves if v not in opened ]

        if u.t_1:
            q_1, t_1 = u.q_1, u.t_1
            q_2, t_2 = u.q_2, u.t_2
        else:
            q_1, t_1 = self.compute_path_flow(u.path_1)
            q_2, t_2 = self.compute_path_flow(u.path_2)
            u.q_1 = q_1
            u.t_1 = t_1
            u.q_2 = q_2
            u.t_2 = t_2

        potential = 0
        for v in still_closed:
            potential += self.Qgas[v] * (max(t_1, t_2) - 1)
        if cost - potential > cost_min:
            return actions

        for v1, v2 in permutations(still_closed, 2):
            path_1 = u.path_1.copy()
            path_2 = u.path_2.copy()
            path_1.append(v1)
            path_2.append(v2)
            dq_1, dt_1 = self.compute_path_step(t_1, u.path_1[-1], v1)
            dq_2, dt_2 = self.compute_path_step(t_2, u.path_2[-1], v2)
            action = ActionNode(path_1, path_2)
            action.q_1 = q_1 + dq_1
            action.t_1 = t_1 + dt_1
            action.q_2 = q_2 + dq_2
            action.t_2 = t_2 + dt_2
            dq = dq_1 + dq_2
            actions.append((action, -dq))

        return actions

    def compute_path_step(self, t1, v1, v2):
        d = self.network[v1][v2][0]
        q = self.Qgas[v2] * (t1 - d - 1)
        return q, -(d + 1)

    def compute_path_flow(self, path):
        Qtotal = 0
        time = self.time_start
        for v1, v2 in zip(path[:-1], path[1:]):
            d = self.network[v1][v2][0]
            time = time - d - 1
            Qtotal += self.Qgas[v2] * time
        return Qtotal, time

    def is_done(self, u):
        for path in [u.path_1, u.path_2]:
            t = self.time_start
            for v1, v2 in zip(path[:-1], path[1:]):
                t -= self.network[v1][v2][0] + 1
            if t <= 0:
                return True
        return False


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


def list_all_paths(network):
    paths = defaultdict(dict)
    for src in network.keys():
        for dest in network.keys():
            if src == dest:
                continue
            path, dist = dijkstra(network, src, dest)
            print(f"dij: {src}, {dest}, {dist}")
            paths[src][dest] = dist, path
    return paths

def main(filename):
    network, Qgas = read(filename)
    print(network, Qgas)
    valve_paths = list_all_paths(network)
    print(valve_paths)

    G = ActionGraph(valve_paths, Qgas, 26)

    print("good valves = ", len(G.good_valves), G.good_valves)
    valves_start = { k: False for k in Qgas.keys() }
    start = ActionNode(["AA"], ["AA"])

    is_done = lambda u: False

    path, cost = dijkstra2(G, start, is_done, debug_freq=1000)

    print("path = ")
    for u in path:
        print(u)

    print("cost = ", cost)


if __name__ == "__main__":
    import sys
    main(sys.argv[1])
