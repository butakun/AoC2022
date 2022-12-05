def read(filename):
    f = open(filename)

    stack_lines = []
    for line in f:
        if line.strip()[0] == '[':
            stack_lines.append(line)
        else:
            stack_ids = [int(i) for i in line.strip().split(" ") if len(i) > 0]
            break
    num_stacks = len(stack_ids)
    
    stacks = [[] for _ in range(num_stacks)]
    for l in reversed(stack_lines):
        for i in range(num_stacks):
            item = l[1 + 4 * i]
            if item != " ":
                stacks[i].append(item)
    print(stacks)

    moves = []
    for line in f:
        tokens = line.strip().split(" ")
        if len(tokens) < 6:
            continue
        n, fr, to = int(tokens[1]), int(tokens[3]), int(tokens[5])
        moves.append((n, fr, to))
    return stacks, moves

def main(filename):
    stacks, moves = read(filename)

    for n, fr, to in moves:
        for i in range(n):
            stacks[to - 1].append(stacks[fr - 1].pop())
        print(stacks)

    print("".join([stack[-1] for stack in stacks]))


if __name__ == "__main__":
    import sys
    main(sys.argv[1])
