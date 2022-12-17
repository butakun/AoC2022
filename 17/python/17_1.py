SHAPES = [
"""
####
"""
,
"""
.#.
###
.#.
"""
,
"""
..#
..#
###
"""
,
"""
#
#
#
#
"""
,
"""
##
##
"""
]

import numpy as np

def build_shapes():
    blocks = []
    for lines in SHAPES:
        block = [ [0 if c == "." else 1 for c in line] for line in lines.strip().split("\n") ]
        block = np.flip(np.array(block), axis=0)
        blocks.append(block)
    
    # profile shape. each is [bottom, top]
    profiles = [
            [[0,0,0,0], [0,0,0,0]],
            [[1,0,1], [1,0,1]],
            [[0,0,0], [2,2,0]],
            [[0], [0]],
            [[0,0], [0,0]]
            ]
    return blocks, profiles


def read_wind(filename):
    with open(filename) as f:
        winds = [ c for c in f.readline().strip() ]
    return winds


def match(xpos, floor, profile):
    # ..@....
    # .@@@...
    # ..@....
    # ....#..
    # ....#..
    # ##..##.
    # ##.###.
    # -------
    # floor = [2,2,4,3,0,2,4]
    # profile = [1,0,1],[1,0,1], bottom-left pos = 1
    #
    # result is
    #
    # ..@.#..
    # .@@@#..
    # ##@.##.
    # ##.###.
    # -------
    # new floor =[3,2,1,2,0,2,2]

    floor_reverse = floor.max() - floor  # [2,2,0,1,4,2,0]

def can_fit(grid, shape, pos):
    # pos is bottom left of the shape

    if pos.min() < 0:
        return False

    h, w = shape.shape
    if (pos[1] + w) > grid.shape[1]:
        return False

    terrain = grid[pos[0]:pos[0]+h,pos[1]:pos[1]+w]
    s = terrain + shape
    return np.all(s <= 1)


def place_shape(grid, shape, pos):
    if pos.min() < 0:
        return False
    h, w = shape.shape
    terrain = grid[pos[0]:pos[0]+h,pos[1]:pos[1]+w] 
    terrain[:, :] += shape[:, :]


def show(grid, h_min, h_max, shape, pos):
    p = pos - np.array([h_min, 0])
    view = grid[h_min:h_max,:].copy()
    if shape is not None:
        h, w = shape.shape
        view[p[0]:p[0]+h,p[1]:p[1]+w] += shape * 2
    for line in reversed(view):
        print("".join(["." if c == 0 else "#" if c == 1 else "@" for c in line]))
    #print(np.flip(view, 0))


def floor_height(grid):
    h = np.where(np.all(grid == 0, axis=1))[0][0]
    return h


def main(filename):
    winds = read_wind(filename)
    shapes, profiles = build_shapes()
    print(shapes)

    floor = np.zeros((7), np.uint32)

    grid = np.zeros((2023 * 4 + 3 + 4, 7), np.int8)
    #grid = np.zeros((20, 7), np.int8)

    pos = np.array([0, 0])
    delta_x = np.array([0, 1])
    delta_y = np.array([1, 0])

    """
    hf = floor_height(grid)
    print("floor = ", hf)

    ok = can_fit(grid, shapes[0], pos)
    print(ok)
    place_shape(grid, shapes[0], pos)
    print(np.flip(grid[:10, :], 0))

    pos += delta_y
    ok = can_fit(grid, shapes[1], pos)
    print(ok)
    place_shape(grid, shapes[1], pos)
    print(np.flip(grid[:10, :], 0))

    hf = floor_height(grid)
    print("floor = ", hf)
    return
    """

    grid[:, :] = 0
    hf = floor_height(grid)
    iblock = 0
    shape = shapes[iblock]
    pos = np.array([hf + 3, 2])
    print(f"initial pos = {pos}")
    time = 0
    while True:
        # wind
        wind = winds[time % len(winds)]
        pos_next = pos.copy()
        if wind == "<" and pos[1] > 0:
            pos_next -= delta_x
        elif wind == ">" and (pos[1] + shape.shape[1] <= 7):
            pos_next += delta_x

        if can_fit(grid, shape, pos_next):
            pos = pos_next
        print(f"after wind {wind}, pos = {pos}")
        #hf = floor_height(grid)
        #show(grid, 0, hf + 10, shape, pos)

        # fall
        pos_next = pos.copy()
        pos_next -= delta_y
        if can_fit(grid, shape, pos_next):
            pos = pos_next
        else:
            print("landed")
            place_shape(grid, shape, pos)
            iblock += 1
            shape = shapes[iblock % len(shapes)]
            hf = floor_height(grid)
            pos = np.array([hf + 3, 2])
            print(f"#### new rock {iblock}")
            hf = floor_height(grid)
            h_min = max(0, hf - 17)
            h_max = hf + 7
            show(grid, h_min, h_max, shape, pos)
            if iblock > 2021:
                break
        print(f"after fall, pos = {pos}, floort at {hf}")

        time += 1

    print("floor height is now ", hf)
    hf = floor_height(grid)
    h_min = max(0, hf - 17)
    h_max = hf + 7
    show(grid, h_min, h_max, None, pos)

if __name__ == "__main__":
    import sys
    main(sys.argv[1])
