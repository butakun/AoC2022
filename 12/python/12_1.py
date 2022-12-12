from dijkstra import dijkstra, a_star


class Graph(object):
    def __init__(self, grid):
        self.grid = grid
        self.idim = len(grid)
        self.jdim = len(grid[0])

        for i in range(self.idim):
            for j in range(self.jdim):
                if self.grid[i][j] == "S":
                    self.start = (i, j)
                elif self.grid[i][j] == "E":
                    self.goal = (i, j)


    def __getitem__(self, u):
        i0, j0 = u
        current = self.grid[i0][j0]
        if current == "E":
            return []

        nei0 = []
        if i0 > 0:
            nei0.append((i0 - 1, j0))
        if i0 < self.idim - 1:
            nei0.append((i0 + 1, j0))
        if j0 > 0:
            nei0.append((i0, j0 - 1))
        if j0 < self.jdim - 1:
            nei0.append((i0, j0 + 1))

        nei = []
        for i, j in nei0:
            hv = self.grid[i][j]
            if current == "S":
                if hv == "a":
                    nei.append([(i, j), 1])
            else:
                v = "z" if hv == "E"  else hv
                d = ord(v) - ord(current)
                if d <= 1:
                    nei.append([(i, j), 1])
        return nei


class HFunc(object):
    def __init__(self, G):
        self.G = G

    def __call__(self, u):
        di = self.G.goal[0] - u[0]
        dj = self.G.goal[1] - u[1]
        return abs(di) + abs(dj)


def main(filename, method, debug):
    grid = [ [ c for c in line.strip() ] for line in open(filename) ]

    G = Graph(grid)

    if method == "dijkstra":
        path, cost = dijkstra(G, G.start, G.goal, debug_freq=debug)
    elif method == "astar":
        path, cost = a_star(G, G.start, G.goal, HFunc(G), debug_freq=debug)
    else:
        raise ValueError(method)
    print(f"{cost}, {path}, {len(path) - 1} steps")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--method", default="astar")
    parser.add_argument("--debug", type=int, default=0)
    args = parser.parse_args()
    main(args.input, args.method, args.debug)
