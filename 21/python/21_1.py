def read(filename):
    tree = {}
    with open(filename) as f:
        for line in f:
            tokens = line.strip().split()
            name = tokens[0].rstrip(":")
            if len(tokens) == 2:
                data = int(tokens[1])
                children = []
            else:
                data = tokens[2]
                children = [tokens[1], tokens[3]]
            tree[name] = (data, children)
    return tree


def main(filename):
    tree = read(filename)
    print(tree)

    def visit(tree, node):
        data, children = tree[node]
        if not children:
            return data
        v1 = visit(tree, children[0])
        v2 = visit(tree, children[1])
        return int(eval(f"{v1} {data} {v2}"))

    v = visit(tree, "root")
    print(v)

if __name__ == "__main__":
    import sys
    main(sys.argv[1])
