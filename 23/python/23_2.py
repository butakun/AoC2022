import numpy as np
from collections import defaultdict
import logging


def read(filename):
    g = [ [ c for c in line ]  for line in  open(filename).read().splitlines() ]
    print(g)

    elves = set()
    for j in range(len(g)):
        for i in range(len(g[0])):
            if g[j][i] == "#":
                elves.add((i, j))
    print(elves)
    return elves


def scan_around(elves, pos):
    nei = np.zeros((3, 3), np.uint8)
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            p = (pos[0] + di, pos[1] + dj)
            if p in elves:
                nei[di+1, dj+1] = 1
    can_move = [False] * 4  # NSWE
    if np.all(nei[:, 0] == 0):
        can_move[0] = True  # North
    if np.all(nei[:, 2] == 0):
        can_move[1] = True  # South
    if np.all(nei[0, :] == 0):
        can_move[2] = True  # West
    if np.all(nei[2, :] == 0):
        can_move[3] = True  # East
    if all(can_move):
        can_move = [False] * 4

    return can_move


def do_round(elves, first_choice):
    # First half
    proposed = defaultdict(list)

    for pos in elves:
        can_move = scan_around(elves, pos)
        logging.info(f"Elf in {pos} can move in NSWE: {can_move}")
        if any(can_move):
            dstep = [(0,-1), (0,1), (-1,0), (1,0)]
            for iorder in range(4):
                inswe = (first_choice + iorder) % 4
                if can_move[inswe]:
                    dp = dstep[inswe]
                    new_pos = (pos[0] + dp[0], pos[1] + dp[1]) 
                    proposed[new_pos].append(pos)
                    logging.info(f"  and proposed moving NSWE: {iorder} to {new_pos}")
                    break
        else:
            proposed[pos].append(pos)
            logging.info(f"  and proposed staying put at {pos}")

    # Second half
    moved = 0
    new_elves = set()
    for new_pos, elves in proposed.items():
        if len(elves) > 1:
            for old_pos in elves:
                assert old_pos not in new_elves
                new_elves.add(old_pos)
                logging.info(f"Elf staying put at {old_pos}")
        else:
            assert new_pos not in new_elves
            old_pos = elves[0]
            new_elves.add(new_pos)
            if new_pos != old_pos:
                moved += 1
            logging.info(f"Elf at {elves[0]} moved to {new_pos}")

    # End
    first_choice = (first_choice + 1) % 4

    return new_elves, first_choice, moved


def bounding_box(elves):
    elf = next(iter(elves))
    imin, jmin = elf
    imax, jmax = elf
    for elf in elves:
        imin = min(imin, elf[0])
        imax = max(imax, elf[0])
        jmin = min(jmin, elf[1])
        jmax = max(jmax, elf[1])
    return imin, imax, jmin, jmax


def dump(elves):
    imin, imax, jmin, jmax = bounding_box(elves)

    for j in range(jmin, jmax + 1):
        line = ""
        for i in range(imin, imax + 1):
            c = "#" if (i, j) in elves else "."
            line += c
        print(line)

def main(filename):
    elves = read(filename)
    dump(elves)
    print(f"  {len(elves)} elves")
    print()

    first_choice = 0

    i = 1
    while True:
        print(f"Round {i}")
        elves, first_choice, moved = do_round(elves, first_choice)
        #dump(elves)
        print(f"  Round {i}, {moved} elves moved")
        if moved == 0:
            break
        i += 1


if __name__ == "__main__":
    import sys
    main(sys.argv[1])
