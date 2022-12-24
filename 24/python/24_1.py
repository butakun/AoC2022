import numpy as np
from dijkstra import dijkstra


class ActionGraph(object):
    def __init__(self, initial_blizz):
        self.blizzz = [initial_blizz]
        idim, jdim = initial_blizz.shape
        lcm = np.lcm(idim-2, jdim-2)
        self.lcm = lcm
        print(f"generating lcm - 1 ({lcm} - 1) generations of the blizzard config")
        blizz = initial_blizz
        for i in range(lcm - 1):
            blizz = blizzard_one_minute(blizz)
            self.blizzz.append(blizz)

    def __getitem__(self, u):
        blizz_index = u[2]
        blizz_index_next = (blizz_index + 1) % self.lcm
        blizz_next = self.blizzz[blizz_index_next]
        actions = []
        for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]:
            i_, j_ = u[0] + di, u[1] + dj
            if i_ < 0 or i_ > blizz_next.shape[0] - 1:
                continue
            if j_ < 0 or j_ > blizz_next.shape[1] - 1:
                continue
            if blizz_next[i_, j_] == 0 or blizz_next[i_, j_] == 1 << 6:
                actions.append((i_, j_, blizz_index_next))
        return actions

    def get_is_dest_func(self):
        blizz = self.blizzz[0]
        idim, jdim = blizz.shape
        return lambda u: u[0] == idim - 1 and u[1] == jdim - 2


def blizzard_one_minute(grid):
    next_grid = np.zeros_like(grid)
    next_grid[grid == 1] = 1
    next_grid[grid == 1 << 6] = 1 << 6
    next_grid[grid == 1 << 7] = 1 << 7

    idim, jdim = grid.shape
    blizz = np.where(grid >= (1 << 1))
    for i, j in zip(blizz[0], blizz[1]):
        b = grid[i, j]
        mask_next = 0
        if b & (1 << 1):  # >
            i_, j_ = i, j+1
            if grid[i_, j_] == (1 << 0):
                j_ = 1
            next_grid[i_, j_] = next_grid[i_, j_] | (1 << 1)
        if b & (1 << 2) and i > 0:  # ^
            i_, j_ = i-1, j
            if grid[i_, j_] == (1 << 0):
                i_ = idim - 2
            next_grid[i_, j_] = next_grid[i_, j_] | (1 << 2)
        if b & (1 << 3):  # <
            i_, j_ = i, j-1
            if grid[i_, j_] == (1 << 0):
                j_ = jdim - 2
            next_grid[i_, j_] = next_grid[i_, j_] | (1 << 3)
        if b & (1 << 4):  # v
            i_, j_ = i+1, j
            if grid[i_, j_] == (1 << 0):
                i_ = 1
            next_grid[i_, j_] = next_grid[i_, j_] | (1 << 4)
    return next_grid


def char(c):
    if c == 0:
        return "."
    elif c == 1:
        return "#"
    elif c == 1 << 6:
        return "G"
    elif c == 1 << 7:
        return "S"
    elif c in [2, 4, 8, 16]:
        return ">" if c & (1 << 1) else \
            "^" if c & (1 << 2) else \
            "<" if c & (1 << 3) else \
            "v" if c & (1 << 4) else "?"
    else:
        m = 0
        for i in [1, 2, 3, 4]:
            if c & (1 << i):
                m += 1
        return f"{m}"

def dump(grid):
    buf = "\n".join([ "".join([
        char(c)
        for c in line ])
        for line in grid ])
    print(buf)


def read(filename):
    grid = [ [
        0 if c == "." else
        1 << 0 if c == "#" else
        1 << 1 if c == ">" else
        1 << 2 if c == "^" else
        1 << 3 if c == "<" else
        1 << 4 if c == "v" else -1
        for c in line ] for line in open(filename).read().splitlines()]

    grid = np.array(grid, np.uint8)
    #grid[0, 1] = 1 << 7
    #grid[-1, -2] = 1 << 6
    return grid


def main(filename):
    grid = read(filename)
    dump(grid)
    idim, jdim = grid.shape
    lcm = np.lcm(idim - 2, jdim - 2)
    print(idim, jdim, lcm)

    G = ActionGraph(grid)
    u = (0, 1, 0)
    for a in G[u]:
        print("action = ", a)

    is_dest = G.get_is_dest_func()
    path, cost = dijkstra(G, u, is_dest, debug_freq=1)
    print(path)
    print("cost = ", cost)

if __name__ == "__main__":
    import sys
    main(sys.argv[1])
