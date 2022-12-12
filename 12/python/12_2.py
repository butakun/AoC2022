from dijkstra import dijkstra


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
                if hv == "S":
                    v = "a"
                elif hv == "E":
                    v = "z"
                else:
                    v = hv
                d = ord(v) - ord(current)
                if d <= 1:
                    nei.append([(i, j), 1])
        return nei


def main(filename):
    grid = [ [ c for c in line.strip() ] for line in open(filename) ]

    G = Graph(grid)

    starts = []
    for i in range(G.idim):
        for j in range(G.jdim):
            if grid[i][j] == "a" or  grid[i][j] == "S":
                starts.append((i, j))

    paths = []
    for start in starts:
        print(f"start = {start}:")
        path, cost = dijkstra(G, start, G.goal, debug_freq=0)
        if path:
            paths.append((cost, path))
            print(f"start = {start}: {cost}, {len(path) - 1} steps")
        else:
            print("didn't reach dest")

    for cost, path in sorted(paths):
        print(f"{cost}, {len(path) - 1} steps")

if __name__ == "__main__":
    import sys
    main(sys.argv[1])
