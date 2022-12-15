import numpy as np
from collections import defaultdict, deque


def read(filename):
    with open(filename) as f:
        lines = [ line for line in f ]

    sensors = []
    beacons = []
    dists = []
    xmin, ymin, xmax, ymax = 0, 0, 0, 0
    for line in lines:
        x = line.split()[2]
        y = line.split()[3]
        x = int(x.split("=")[1][:-1])
        y = int(y.split("=")[1][:-1])
        ps = [x, y]
        sensors.append(ps)

        x = line.split()[8]
        y = line.split()[9]
        x = int(x.split("=")[1][:-1])
        y = int(y.split("=")[1])
        pb = [x, y]
        beacons.append(pb)

        d = np.abs(np.array(pb) - np.array(ps)).sum()
        dists.append(d)

        xmin = min(xmin, ps[0] - d)
        xmax = max(xmax, ps[0] + d)
        ymin = min(ymin, ps[1] - d)
        ymax = max(ymax, ps[1] + d)

    print(sensors)
    print(beacons)

    sensors = np.array(sensors)
    beacons = np.array(beacons)
    """
    xymins = sensors.min(axis=0)
    xyminb = beacons.min(axis=0)

    ixmins = sensors[:, 0].argmin()
    dxmins = dists[ixmins]
    xmins = sensors[ixmins, 0] - dxmins

    iymins = sensors[:, 1].argmin()
    dymins = dists[iymins]
    ymins = sensors[iymins, 1] - dymins

    ixmaxs = sensors[:, 0].argmax()
    dxmaxs = dists[ixmaxs]
    xmaxs = sensors[ixmaxs, 0] + dxmaxs

    iymaxs = sensors[:, 1].argmax()
    dymaxs = dists[iymaxs]
    ymaxs = sensors[iymaxs, 1] + dymaxs

    xymin = np.array([xymins, xyminb]).min(axis=0)
    xymin[0] = xmins
    xymin[1] = ymins

    xymaxs = sensors.max(axis=0)
    xymaxb = beacons.max(axis=0)
    xymax = np.array([xymaxs, xymaxb]).max(axis=0)
    xymax[0] = xmaxs
    xymax[1] = ymaxs
    """
    xymin = np.array([xmin, ymin])
    xymax = np.array([xmax, ymax])

    print("xymin: ", xymin)
    print("xymax: ", xymax)
    shape = xymax - xymin + np.array([1, 1])
    print("shape: ", shape)

    #grid = np.zeros(shape, np.uint8)

    return shape, xymin, sensors, beacons, dists


def connected_component(G, start, debug=0):
    visited = set([start])
    Q = deque([start])
    while Q:
        u = Q.popleft()
        for v in G[u]:
            if v not in visited:
                Q.append(v)
                visited.add(v)
    return set(visited)


def overlaps(a, b):
    return a[0]-1 <= b[1] and b[0] <= a[1]+1


def union(covered):
    n = len(covered)
    graph = defaultdict(set)
    for i1 in range(n):
        c1 = covered[i1]
        for i2 in range(i1+1,n):
            c2 = covered[i2]
            if overlaps(c1, c2):
                graph[i1].add(i2)
                graph[i2].add(i1)

    groups = []
    grouped = set()
    for i in range(n):
        if i in grouped:
            continue
        comp = connected_component(graph, i)
        grouped.update(comp)
        groups.append(comp)

    ranges = []
    for group in groups:
        imin, imax = None, None
        for l in group:
            r = covered[l]
            if imin is None:
                imin, imax = r
                continue
            imin = min(imin, r[0])
            imax = max(imax, r[1])
        ranges.append([imin, imax])
    return ranges


def check_line(sensors, beacons, dists, shape, xymin, jcheck):
    jcheck_ = jcheck - xymin[1]

    #line = np.zeros((shape[0]), np.uint8)
    line = None

    covered = []
    for i in range(sensors.shape[0]):
        ps = sensors[i, :] - xymin
        pb = beacons[i, :] - xymin
        d = dists[i]
        #print(f"sensor {i} at {ps} as d={d}")
        if abs(jcheck_ - ps[1]) > d:
            continue
        jj = jcheck_
        di = d - abs(jj - ps[1])
        ii = ps[0]
        #line[ii-di:ii+di+1] = 3
        rang = [sensors[i,0]-di, sensors[i,0]+di]
        covered.append(rang)
        #print(f"  d={d}, di={di}, ii={ii}, range=rang: ", line)

    ranges = union(covered)
    ranges.sort()

    return line, ranges


def main(filename, imax):
    shape, xymin, sensors, beacons, dists = read(filename)

    zeros = []
    for j in range(imax+1):
        j_ = j - xymin[1]
        line, ranges = check_line(sensors, beacons, dists, shape, xymin, j)
        #print(f"line {j} ranges = {ranges}")
        if len(ranges) > 1:
            ihole = ranges[0][1]+1
            print("a hole found at ", ihole, j, ihole * 4000000 + j)
            break
        if j % 1000 == 0:
            print("line ", j)


if __name__ == "__main__":
    import sys
    main(sys.argv[1], int(sys.argv[2]))
