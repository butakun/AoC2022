from functools import cmp_to_key


def read(filename):
    packets = []
    for line in open(filename):
        line = line.strip()
        if len(line) == 0:
            continue
        packets.append(eval(line))
    return packets


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
    packets = read(filename)
    packets.append([[2]])
    packets.append([[6]])

    packets.sort(key=cmp_to_key(compare), reverse=True)

    id1, id2 = -1, -1
    for i, packet in enumerate(packets):
        if packet \
            and isinstance(packet, list) \
            and len(packet) == 1 \
            and isinstance(packet[0], list) \
            and len(packet[0]) == 1 :
            if packet[0][0] == 2:
                print("*** id1", packet)
                id1 = i + 1
            elif packet[0][0] == 6:
                print("*** id2", packet)
                id2 = i + 1
    print(id1, id2, id1 * id2)


if __name__ == "__main__":
    import sys
    main(sys.argv[1])
