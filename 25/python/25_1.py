decimal_snafu = [
[2, "2"],
[3, "1="],
[4, "1-"],
[5, "10"],
[6, "11"],
[7, "12"],
[8, "2="],
[9, "2-"],
[10, "20"],
[15, "1=0"],
[20, "1-0"],
[2022, "1=11-2"],
[12345, "1-0---0"],
[314159265, "1121-1110-1=0"],
]

def snafu_to_decimal(snafu):
    decimal = 0
    for i, s in enumerate(reversed(snafu)):
        s_ = 0 if s == "0" else 1 if s == "1" else 2 if s == "2" else -1 if s == "-" else -2
        d = pow(5, i) * s_
        decimal += d
    return decimal

def decimal_to_snafu(decimal):
    snafu = []
    value = decimal
    bump_next = 0
    while True:
        d = value % 5
        if d < 3:
            bump_next = 0
        elif d == 3:
            d = -2
            bump_next = 1
        elif d == 4:
            d = -1
            bump_next = 1

        snafu.append(d)
        value = value // 5 + bump_next
        if value == 0:
            break

    snafu_ = ""
    snafu.reverse()
    for s in snafu:
        if 0 <= s and s < 3:
            snafu_ += f"{s}"
        elif s == -1:
            snafu_ += "-"
        elif s == -2:
            snafu_ += "="
    return snafu_


def debug():
    for decimal, snafu in decimal_snafu:
        mine = decimal_to_snafu(decimal)
        print(f"{mine} == {snafu} ?")
        assert mine == snafu

    for decimal, snafu in decimal_snafu:
        mine = snafu_to_decimal(snafu)
        print(f"{mine} == {decimal} ?")
        assert mine == decimal


def main(filename):
    snafus = open(filename).read().splitlines()

    answer_decimal = sum([snafu_to_decimal(snafu) for snafu in snafus])
    answer = decimal_to_snafu(answer_decimal)
    print(f"answer (decimal) = {answer_decimal}")
    print(f"answer (snafu) = {answer}")

if __name__ == "__main__":
    import sys
    main(sys.argv[1])


"""
4890 % 5 = 0
4890 // 5 = 978
978 % 5 = 3
978 // 5 = 195
195 % 5 = 0
195 // 5 = 39
39 % 5 = 4
39 // 5 = 7
7 % 5 = 2
7 // 5 = 1
1 % 5 = 1
1 // 5 = 0
-> 124030 in base-5
0 -2 1 -1 -2 2 -> 2=-1=0

4890 % 5 = 0
4590 // 5 = 978
978 % 5 = 3 -> -2 (+1)
978 // 5 = 195
196 % 5 = 1
196 // 5 = 39
39 % 5 = 4 = -1 (+1)
39 // 5 = 7
8 % 5 = 3 = -2 (+1)
8 // 5 = 1
2 % 5 = 2
2 // 5 = 0
0 +1 1 -1 -2 2


16 decimal to binary
16 % 2 = 0
16 // 2 = 8
8 % 2 = 0
8 // 2 = 4
4 % 2 = 0
4 // 2 = 2
2 % 2 = 0
2 // 2 = 1
1 % 2 = 1
1 // 2 = 0
"""
