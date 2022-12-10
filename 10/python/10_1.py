def main(filename):
    ops = [ line.strip().split(" ") for line in open(filename) ]
    ops = [ [op[0], int(op[1]) if len(op) == 2 else 0] for op in ops ]
    print(ops)

    X = 1
    i = 1
    iwait = 0
    accum = 0
    op, v = "noop", 0
    while i < 221:
        if iwait == 0:
            if op == "addx":
                print(f"{op} {v}")
                X += v
            else:
                print(f"{op} {v}")
            op, v = ops.pop(0)
            if op == "addx":
                iwait = 2
            else:
                iwait = 1
        print(i, X, iwait)

        if i in [20, 60, 100, 140, 180, 220]:
            print(f"i * X = {i * X}")
            accum += i * X

        iwait -= 1
        i += 1

    print(accum)


if __name__ == "__main__":
    import sys
    main(sys.argv[1])
