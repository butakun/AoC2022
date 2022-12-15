import numpy as np


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


def main(filename, jcheck):
    shape, xymin, sensors, beacons, dists = read(filename)

    jcheck_ = jcheck - xymin[1]

    line = np.zeros((shape[0]), np.uint8)

    for i in range(sensors.shape[0]):
        ps = sensors[i, :] - xymin
        pb = beacons[i, :] - xymin
        d = dists[i]
        print(f"sensor {i}")
        if abs(jcheck_ - ps[1]) > d:
            continue
        jj = jcheck_
        di = d - abs(jj - ps[1])
        ii = ps[0]
        #grid[ii-di:ii+di+1, jj] = 3
        line[ii-di:ii+di+1] = 3

    for i in range(sensors.shape[0]):
        ps = sensors[i, :] - xymin
        pb = beacons[i, :] - xymin
        if ps[1] == jcheck_:
            line[ps[0]] = 1
        if pb[1] == jcheck_:
            line[pb[0]] = 2
        #grid[ps[0], ps[1]] = 1
        #grid[pb[0], pb[1]] = 2

    #line = grid[:, jcheck_]

    print(line)
    n_sensors = (line == 1).sum()
    n_beacons = (line == 2).sum()
    n_voids = (line == 3).sum()
    print(f"sensors {n_sensors}, beacons {n_beacons}, voids = {n_voids}")
    print(n_voids + n_sensors)


if __name__ == "__main__":
    import sys
    main(sys.argv[1], int(sys.argv[2]))
