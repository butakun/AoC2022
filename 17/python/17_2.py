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


class Grid(object):
    def __init__(self, initial_height=1000):
        self.grid = np.zeros((initial_height, 7), np.int8)
        self._set_new_virtual_floor(0)
        self._column_height = 0

    def can_fit(self, shape, pos):
        # pos is bottom left of the shape
        pos_rel = pos - self.origin
        if pos_rel.min() < 0:
            return False
        h, w = shape.shape
        if (pos_rel[1] + w) > self.grid.shape[1]:
            return False

        terrain = self.grid[pos_rel[0]:pos_rel[0]+h, pos_rel[1]:pos_rel[1]+w]
        s = terrain + shape
        return np.all(s <= 1)

    def place_shape(self, shape, pos):
        pos_rel = pos - self.origin
        if pos.min() < 0:
            return False
        h, w = shape.shape
        terrain = self.grid[pos_rel[0]:pos_rel[0]+h, pos_rel[1]:pos_rel[1]+w]
        terrain[:, :] += shape[:, :]

    def compute_column_height(self):
        h = np.where(np.all(self.grid == 0, axis=1))[0][0]
        h += self.virtual_floor
        self._column_height = h

    def update_column_height(self, h):
        self._column_height = h

    def column_height(self):
        return self._column_height

    def find_new_virtual_floor(self):
        skyline = np.zeros((self.grid.shape[1]), np.int32)
        for j in range(self.grid.shape[1]):
            blocked = self.grid[:, j] == 1
            if not np.any(blocked):
                skyline[j] = self.virtual_floor
            else:
                skyline[j] = np.where(blocked)[0][-1] + self.virtual_floor + 1
        print("skyline = ", skyline)
        return skyline.min()

    def _set_new_virtual_floor(self, vf):
        self.virtual_floor = vf
        self.origin = np.array([vf, 0])

    def move_grid(self):
        vf = self.find_new_virtual_floor()
        vf_rel = vf - self.virtual_floor
        if vf_rel == 0:
            print("can't move the grid as virtual floor is ", vf, vf_rel)
            return
        print("moving grid with new virtual floor at ", vf, vf_rel)
        grid_new = np.zeros(self.grid.shape, np.int8)
        grid_new[:-vf_rel, :] = self.grid[vf_rel:,:]
        self.grid = grid_new
        self._set_new_virtual_floor(vf)

    def show(self, shape=None, pos=None, h=20):
        view_height = 7 + h
        ch = self._column_height - self.virtual_floor
        h_min = max(0, ch - h)
        h_max = h_min + view_height

        view = self.grid[h_min:h_max,:].copy()

        if shape is not None:
            pos_rel = pos - self.origin
            p = pos_rel - np.array([h_min, 0])
            h, w = shape.shape
            view[p[0]:p[0]+h,p[1]:p[1]+w] += shape * 2
        for line in reversed(view):
            print("".join(["." if c == 0 else "#" if c == 1 else "@" for c in line]))


def check_pattern(iblock, grid, shape, pos, winds, time):
    ch = grid.column_height()
    print(f"CHECKING PATTERN: iblock {iblock}, time {time}, {time % len(winds)}, ch {ch}: {grid.grid[ch-1,:]}")


def main(filename):
    winds = read_wind(filename)
    shapes, profiles = build_shapes()

    n_lines = 50000
    grid = Grid(initial_height=n_lines)

    grid.show()

    iblock = 0
    delta_x = np.array([0, 1])
    delta_y = np.array([1, 0])
    shape = shapes[iblock]
    pos = np.array([3, 2])
    print(f"initial pos = {pos}")
    time = 0
    check_pattern(iblock, grid, shape, pos, winds, time)
    while True:
        # wind
        wind = winds[time % len(winds)]
        pos_next = pos.copy()
        if wind == "<" and pos[1] > 0:
            pos_next -= delta_x
        elif wind == ">" and (pos[1] + shape.shape[1] <= 7):
            pos_next += delta_x

        if grid.can_fit(shape, pos_next):
            pos = pos_next
        #print(f"after wind {wind}, pos = {pos}")

        # fall
        pos_next = pos.copy()
        pos_next -= delta_y
        if grid.can_fit(shape, pos_next):
            pos = pos_next
        else:
            #print("landed")
            grid.place_shape(shape, pos)
            shape_top = pos[0] + shape.shape[0]
            new_column_height = max(shape_top, grid.column_height())
            grid.update_column_height(new_column_height)
            #print("set the new column height to ", new_column_height)

            # new shape
            iblock += 1
            shape = shapes[iblock % len(shapes)]
            pos = np.array([grid.column_height() + 3, 2])
            if iblock % len(shapes) == 0:
                check_pattern(iblock, grid, shape, pos, winds, time)
            if iblock % 1000 == 0:
                print(f"#### new rock {iblock} at {pos}")
            #grid.show(shape, pos)

            if grid.column_height() > (grid.grid.shape[0] + grid.virtual_floor - 20):
                #print("moving internal grid", grid.column_height(), grid.grid.shape[0], grid.virtual_floor)
                grid.move_grid()
                #grid.show(shape, pos)

            if iblock >= 10000:
                break
        #print(f"after fall, pos = {pos}, column at {grid.column_height()}")

        time += 1

    vf = grid.find_new_virtual_floor()
    print("virtual floor = ", vf)
    print("column height =", grid.column_height(), grid._column_height)
    grid.show(shape, pos)

if __name__ == "__main__":
    import sys
    main(sys.argv[1])
