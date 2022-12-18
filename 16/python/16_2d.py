from dijkstra import dijkstra, dijkstra2, a_star2
from collections import defaultdict


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
            paths[src][dest] = dist, path
    return paths


def main(filename):
    network, Qgas = read(filename)
    print(network, Qgas)
    good_valve_flows = { k: v for k, v in Qgas.items() if v > 0 }
    good_valve_names = sorted(good_valve_flows.keys())
    print(good_valve_flows)
    print(good_valve_names)
    valve_paths = list_all_paths(network)
    print(valve_paths)

    good_valve_network = {
            u: { v: t for v, (t, _) in vv.items() if v in good_valve_names }
            for u, vv in valve_paths.items() if u in good_valve_names or u == "AA"
            }
    print(good_valve_network)

    def visit(u, valve_state, time_remaining, Q, Qmax):
        state_key = tuple(valve_state)
        Qmax_sofar = Qmax.get(state_key, 0)
        Qmax[state_key] = max(Qmax_sofar, Q)
        if time_remaining <= 0 or all(valve_state):
            return
        for v, q in good_valve_flows.items():
            iv = good_valve_names.index(v)
            if not valve_state[iv]:
                valve_state_next = valve_state.copy()
                valve_state_next[iv] = True
                time_remaining_next = time_remaining - good_valve_network[u][v] - 1
                Qnext = Q + time_remaining_next * q
                visit(v, valve_state_next, time_remaining_next, Qnext, Qmax)

    initial_state = [False] * len(good_valve_names)
    Qmax = {}
    visit("AA", initial_state, 26, 0, Qmax)

    pretty_state = lambda state: "".join(["*" if c else "." for c in state])

    Qmax_sorted = sorted([ [qmax, state] for state, qmax in Qmax.items() ])
    for qmax, state in Qmax_sorted:
        print(f"{pretty_state(state)}: {qmax}")

    Qmax_combined = 0
    state_pair = None
    for state1, qmax1 in Qmax.items():
        for state2, qmax2 in Qmax.items():
            qmax = qmax1 + qmax2
            if qmax < Qmax_combined:
                continue
            combined_state = [ s1 and s2 for s1, s2 in zip(state1, state2) ]
            if any(combined_state):
                continue
            if qmax > Qmax_combined:
                Qmax_combined = qmax
                state_pair = state1, state2
    print("Qmax combined = ", Qmax_combined)
    print(f"state1: {pretty_state(state_pair[0])}")
    print(f"state1: {pretty_state(state_pair[1])}")


if __name__ == "__main__":
    import sys
    main(sys.argv[1])
