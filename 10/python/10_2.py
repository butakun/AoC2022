def main(filename):
    ops = [ line.strip().split(" ") for line in open(filename) ]
    ops = [ [op[0], int(op[1]) if len(op) == 2 else 0] for op in ops ]
    print(ops)

    X = 1
    i = 1
    iwait = 0
    op, v = "noop", 0
    lines = []
    line = ""
    while i < 241:
        if iwait == 0:
            if op == "addx":
                X += v
            op, v = ops.pop(0)
            if op == "addx":
                iwait = 2
            else:
                iwait = 1
        print(i, X, iwait, op, v)
        x = (i - 1) % 40
        if abs(x - X) <= 1:
            line += "#"
        else:
            line += "."

        if i % 40 == 0:
            lines.append(line)
            line = ""

        iwait -= 1
        i += 1

    for line in lines:
        print(line)


if __name__ == "__main__":
    import sys
    main(sys.argv[1])
