import numpy as np
from collections import defaultdict


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

    return can_move


def do_round(elves, first_choice):
    # First half
    proposed = defaultdict(list)

    for pos in elves:
        can_move = scan_around(elves, pos)
        print(f"Elf in {pos} can move in NSWE: {can_move}")
        if any(can_move):
            dstep = [(0,-1), (0,1), (-1,0), (1,0)]
            for iorder in range(4):
                inswe = (first_choice + iorder) % 4
                if can_move[inswe]:
                    dp = dstep[inswe]
                    new_pos = (pos[0] + dp[0], pos[1] + dp[1]) 
                    proposed[new_pos].append(pos)
                    print(f"  and proposed moving NSWE: {iorder} to {new_pos}")
                    break
        else:
            proposed[pos].append(pos)
            print(f"  and proposed staying put at {pos}")

    # Second half
    new_elves = set()
    for new_pos, elves in proposed.items():
        if len(elves) > 1:
            for old_pos in elves:
                assert old_pos not in new_elves
                new_elves.add(old_pos)
                print(f"Elf staying put at {old_pos}")
        else:
            assert new_pos not in new_elves
            new_elves.add(new_pos)
            print(f"Elf at {elves[0]} moved to {new_pos}")

    # End
    first_choice = (first_choice + 1) % 4

    return new_elves, first_choice


def dump(elves):
    elf = next(iter(elves))
    imin, jmin = elf
    imax, jmax = elf
    for elf in elves:
        imin = min(imin, elf[0])
        imax = max(imax, elf[0])
        jmin = min(jmin, elf[1])
        jmax = max(jmax, elf[1])

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

    for i in range(3):
        print(f"Round {i}")
        elves, first_choice = do_round(elves, first_choice)
        dump(elves)
        print(f"  {len(elves)} elves")


if __name__ == "__main__":
    import sys
    main(sys.argv[1])
