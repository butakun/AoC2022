from dijkstra import dijkstra, dijkstra2
from collections import defaultdict
from itertools import permutations


class ActionNode(object):
    def __init__(self, valve1, valve2, time_remaining, valves):
        self.valve1 = valve1
        self.valve2 = valve2
        self.time_remaining = time_remaining
        self.valves = valves

    def __hash__(self):
        return hash((self.valve1, self.valve2, self.time_remaining, tuple(sorted(self.valves.items()))))

    def __repr__(self):
        return f"{self.valve1}, {self.valve2}, {self.time_remaining}, {self.valves}"


class ActionGraph(object):
    """ u = (room, time_remaining, valves) """
    def __init__(self, network, Qgas):
        self.network = network
        self.good_valves = [ k for k, v in Qgas.items() if v > 0 ]
        self.Qgas = Qgas

    def next_actions(self, u, cost, cost_min):
        actions = []

        cost_improvement = 0
        still_closed = [ v for v in self.good_valves if u.valves[v] == False ]
        for v in still_closed:
            cost_improvement -= self.Qgas[v] * u.time_remaining
        cost_possible = cost + cost_improvement
        if cost_min < cost_possible:
            return actions

        if u.valve1 in still_closed:
            # we open valve 1 first
            target_1 = u.valve1
            cost = self.Qgas[target_1] * (u.time_remaining - 1)
            valves_next = u.valves.copy()
            valves_next[target_1] = True
            for target_2 in still_closed:
                if target_2 == u.valve1:
                    continue
                target_2 = self.network[u.valve2][target_2][1][1]
                action_next = ActionNode(target_1, target_2, u.time_remaining - 1, valves_next)
                actions.append((action_next, -cost))
            return actions
        elif u.valve2 in still_closed:
            # we open valve 2 first
            target_2 = u.valve2
            cost = self.Qgas[target_2] * (u.time_remaining - 1)
            valves_next = u.valves.copy()
            valves_next[target_2] = True
            for target_1 in still_closed:
                if target_1 == u.valve2:
                    continue
                target_1 = self.network[u.valve1][target_1][1][1]
                action_next = ActionNode(target_1, target_2, u.time_remaining - 1, valves_next)
                actions.append((action_next, -cost))
            return actions

        for target_1, target_2 in permutations(still_closed, 2):
            dist_1, path_1 = self.network[u.valve1][target_1]
            dist_2, path_2 = self.network[u.valve2][target_2]

            open_1, open_2 = False, False
            if dist_1 == dist_2:
                dist_1 += 1
                dist_2 += 1
                open_1 = True
                open_2 = True
            elif dist_1 < dist_2:
                open_1 = True
                dist_1 += 1  # we open target 1
                target_2 = self.network[u.valve2][target_2][1][dist_1]
                dist_2 = dist_1
            elif dist_2 < dist_1:
                open_2 = True
                dist_2 += 1  # we open target 2
                target_1 = self.network[u.valve1][target_1][1][dist_2]
                dist_1 = dist_2
            assert(dist_1 == dist_2)

            valves_next = u.valves.copy()
            cost_next = 0
            if open_1:
                valves_next[target_1] = True
                cost_next += self.Qgas[target_1] * (u.time_remaining - dist_1)
            if open_2:
                valves_next[target_2] = True
                cost_next += self.Qgas[target_2] * (u.time_remaining - dist_2)

            action_next = ActionNode(target_1, target_2, u.time_remaining - dist_1, valves_next)
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

    G = ActionGraph(valve_paths, Qgas)

    valves_start = { k: False for k in Qgas.keys() }
    start = ActionNode("AA", "AA", 26, valves_start)

    is_done = lambda u: u.time_remaining <= 0

    path, cost = dijkstra2(G, start, is_done, debug_freq=1000)

    print("path = ")
    for u in path:
        print(u)

    print("cost = ", cost)


if __name__ == "__main__":
    import sys
    main(sys.argv[1])
