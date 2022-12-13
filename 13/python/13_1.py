def read(filename):
    pairs = []
    pair = []
    for line in open(filename):
        line = line.strip()
        if len(line) == 0:
            assert pair
            pairs.append(pair)
            pair = []
        else:
            pair.append(eval(line))
    if pair:
        assert pair
        pairs.append(pair)

    return pairs


def compare(left, right):
    l = isinstance(left, list)
    r = isinstance(right, list)
    if not l and r:
        return compare([left], right)
    elif l and not r:
        return compare(left, [right])
    elif not l and not r:
        if left == right:
            return 0
        elif left < right:
            return 1
        elif left > right:
            return -1
    elif l and r:
        llen = len(left)
        rlen = len(right)
        c = 0
        for i in range(min(llen, rlen)):
            c = compare(left[i], right[i])
            if c != 0:
                break
        if c == 0:
            if llen == rlen:
                return 0
            elif llen < rlen:
                return 1
            elif llen > rlen:
                return -1
        else:
            return c


def main(filename):
    pairs = read(filename)
    sum = 0
    for ipair, pair in enumerate(pairs):
        print(pair[0])
        print(pair[1])
        c = compare(*pair)
        assert c != 0
        print("verdict = ", c)
        print()
        if c == 1:
            sum += (ipair + 1)

    print(f"sum = {sum}")


if __name__ == "__main__":
    import sys
    main(sys.argv[1])
