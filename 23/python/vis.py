import pickle
import cv2
import numpy as np


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


def main():
    rounds = pickle.load(open("elves.pkl", "rb"))

    imin, imax, jmin, jmax = bounding_box(rounds[-1])
    print(imin, imax, jmin, jmax)

    R = 3
    w = (imax - imin + 1) * 2 * R
    h = (jmax - jmin + 1) * 2 * R

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter("elves.mp4", fourcc, 20, (w, h))

    dormant = 20
    for i in range(dormant):
        rounds.append(rounds[-1].copy())

    ages = dict()
    old = set()
    for i, elves in enumerate(rounds):
        frame = np.zeros((h, w, 3), np.uint8)
        for x, y in elves:
            if (x, y) in ages:
                ages[(x, y)] = min(ages[(x, y)] + 1, dormant)
            else:
                ages[(x, y)] = 0

            xi = (dormant - ages[(x, y)]) / dormant
            brightness = int((1.0 - xi) * 128 + xi * 255)
            #print(xi, brightness)
            color = (int(brightness), int(brightness), int(brightness))

            px = 2 * R * (x - imin) + R
            py = 2 * R * (y - jmin) + R
            cv2.circle(frame, (px, py), R, color, cv2.FILLED)
        writer.write(frame)
        cv2.imwrite(f"frame.{i:04d}.jpg", frame)

        for x, y in old:
            if (x, y) not in elves:
                ages.pop((x, y))

        old = elves


if __name__ == "__main__":
    main()
