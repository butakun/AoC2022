from dijkstra import dijkstra, dijkstra2
from collections import defaultdict


class ActionNode(object):
    def __init__(self, valve, time_remaining, valves):
        self.valve = valve
        self.time_remaining = time_remaining
        self.valves = valves

    def __hash__(self):
        return hash((self.valve, self.time_remaining, tuple(sorted(self.valves.items()))))

    def __repr__(self):
        return f"{self.valve}, {self.time_remaining}, {self.valves}"

class ActionGraph(object):
    """ u = (room, time_remaining, valves) """
    def __init__(self, network, Qgas):
        self.network = network
        self.good_valves = [ k for k, v in Qgas.items() if v > 0 ]
        self.Qgas = Qgas

    def next_actions(self, u, cost, cost_min):
        actions = []

        cost_improvement = 0
        for nei_valve, _ in self.network[u.valve]:
            if nei_valve not in self.good_valves:
                continue
            if not u.valves[nei_valve]:
                #dist = self.network[u.valve][nei_valve]
                cost_improvement -= self.Qgas[nei_valve] * u.time_remaining
        cost_possible = cost + cost_improvement
        if cost_min < cost_possible:
            return actions

        for nei_valve, dist in self.network[u.valve]:
            if nei_valve not in self.good_valves:
                continue
            
            if u.time_remaining >= dist + 1 and not u.valves[nei_valve]:
                valves_next = u.valves.copy()
                valves_next[nei_valve] = True
                action_next = ActionNode(nei_valve, u.time_remaining - dist - 1, valves_next)
                cost_next = self.Qgas[nei_valve] * (u.time_remaining - dist - 1)
                actions.append((action_next, -cost_next))

        return actions


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
    paths = defaultdict(list)
    for src in network.keys():
        for dest in network.keys():
            if src == dest:
                continue
            path, dist = dijkstra(network, src, dest)
            print(f"dij: {src}, {dest}, {dist}")
            paths[src].append((dest, dist))
    return paths

def main(filename):
    network, Qgas = read(filename)
    print(network, Qgas)
    valve_paths = list_all_paths(network)

    G = ActionGraph(valve_paths, Qgas)

    valves_start = { k: False for k in Qgas.keys() }
    start = ActionNode("AA", 30, valves_start)

    is_done = lambda u: u.time_remaining <= 0

    path, cost = dijkstra2(G, start, is_done, debug_freq=1000)

    print("path = ")
    for u in path:
        print(u)

    print("cost = ", cost)


if __name__ == "__main__":
    import sys
    main(sys.argv[1])
