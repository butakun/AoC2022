def find_marker(line):
    for i, c in enumerate(line):
        i0 = max(i - 13, 0)
        last = line[i0:i+1]
        four = set(last)
        if len(four) == 14:
            return i + 1
    raise ValueError


def main(filename):
    with open(filename) as f:
        lines = [l.strip() for l in f]

    for line in lines:
        count = find_marker(line)
        print(count)


import sys
main(sys.argv[1])
