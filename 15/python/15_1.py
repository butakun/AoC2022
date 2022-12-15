import numpy as np


def read(filename):
    with open(filename) as f:
        lines = [ line for line in f ]

    sensors = []
    beacons = []
    dists = []
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

    print(sensors)
    print(beacons)

    sensors = np.array(sensors)
    beacons = np.array(beacons)
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

    print("xymin: ", xymin)
    print("xymax: ", xymax)
    shape = xymax - xymin + np.array([1, 1])
    print("shape: ", shape)

    grid = np.zeros(shape, np.uint8)

    for i in range(sensors.shape[0]):
        ps = sensors[i, :] - xymin
        pb = beacons[i, :] - xymin
        d = np.abs(pb - ps).sum()
        for dj, ii in enumerate(range(ps[0]-d, ps[0]+d+1)):
            if ii < 0 or ii >= shape[0]:
                continue
            if dj > d:
                dj = d - (dj - d)
            for jj in range(ps[1]-dj, ps[1]+dj+1):
                #print("idj: ", ii, jj, dj)
                if jj < 0 or jj >= shape[1]:
                    continue
                grid[ii, jj] = 3

    for i in range(sensors.shape[0]):
        ps = sensors[i, :] - xymin
        pb = beacons[i, :] - xymin
        grid[ps[0], ps[1]] = 1
        grid[pb[0], pb[1]] = 2

    return grid, xymin


def main(filename):
    grid, xymin = read(filename)

    print(grid[0-xymin[0]:25-xymin[0],0-xymin[1]:23-xymin[1]].T)

    icheck = 10
    icheck = 2000000
    line = grid[icheck - xymin[0], :]

    print(line)
    print((line == 3).sum() + (line == 1).sum())


if __name__ == "__main__":
    import sys
    main(sys.argv[1])
