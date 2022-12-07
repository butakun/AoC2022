from pprint import pprint


def read_dir(lines, node):
    for j, line in enumerate(lines):
        tokens = line.strip().split(" ")
        if tokens[0] == "$":
            if tokens[1] == "cd":
                dirname = tokens[2]
                if dirname == "..":
                    node = node[".."]
                else:
                    node = node[dirname]
            elif tokens[1] == "ls":
                pass
            else:
                raise ValueError(line)
        else:
            if tokens[0] == "dir":
                node[tokens[1]] = {"..": node}
            else:
                node[tokens[1]] = int(tokens[0])


def calc_size(node, book, path):
    siz = 0
    for k, v in node.items():
        if k == "..":
            continue
        if isinstance(v, dict):
            path.append(k)
            siz_child = calc_size(v, book, path)
            siz += siz_child
            key = "/".join(path)
            assert key not in book
            book[key] = siz_child
            path.pop()
            continue
        siz += v
    return siz


def main(filename):
    lines = [l for l in open(filename)]
    path = []
    tree = {"/": {}, "..": None}
    read_dir(lines, tree)
    pprint(tree)

    book = {}
    path = []
    siz = calc_size(tree, book, path)
    pprint(book)
    root = book["/"]
    total = 70000000

    candidates = [(k, v) for k, v in book.items() if (total - root + v) >= 30000000]
    pprint(candidates)
    print(min(candidates, key=lambda v:v[1]))


if __name__ == "__main__":
    import sys
    main(sys.argv[1])
