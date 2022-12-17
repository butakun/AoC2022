def read_wind(filename):
    with open(filename) as f:
        winds = f.readline().strip()
    return winds


def main(filename):
    winds = read_wind(filename)

    print(len(winds))
    for pat_len in range(10, len(winds)):
        pat = winds[0:pat_len]
        print(f"checking {pat_len}:")
        for i in range(pat_len, len(winds) - pat_len):
            if winds[i:i+pat_len] == pat:
                print(f"found at {i}: {winds[i:i+pat_len]}")


if __name__ == "__main__":
    import sys
    main(sys.argv[1])
