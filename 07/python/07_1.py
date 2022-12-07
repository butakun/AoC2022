from pprint import pprint


def read(filename):

    def read_dir(lines, path, tree, node):
        print(f"PATH {path}")
        pprint(f"TREE {tree}")

        for j, line in enumerate(lines):
            tokens = line.strip().split(" ")
            if tokens[0] == "$":
                if tokens[1] == "cd":
                    if tokens[2] == "..":
                        print("popping:", path)
                        path.pop()
                        node = node[".."]
                    else:
                        path.append(tokens[2])
                        node = node[tokens[2]]
                elif tokens[1] == "ls":
                    pass
                else:
                    raise ValueError(line)
            else:
                if tokens[0] == "dir":
                    node[tokens[1]] = {"..": node}
                else:
                    node[tokens[1]] = int(tokens[0])
                print("adding ", path[-1], " : ", tokens[1])

    lines = [l for l in open(filename)]
    path = []
    tree = {"/": {}, "..": None}
    read_dir(lines, path, tree, tree)
    pprint(tree)

    def calc_size(node, book):
        siz = 0
        for k, v in node.items():
            if k == "..":
                continue
            if isinstance(v, dict):
                siz_child = calc_size(v, book)
                siz += siz_child
                if siz_child <= 100000:
                    count = 0
                    while True:
                        key = f"{k}.{count}"
                        if key not in book:
                            break
                        print(key, "exists")
                        count += 1
                    book[key] = siz_child
                continue
            siz += v
        return siz

    book = {}
    siz = calc_size(tree, book)
    pprint(book)

    print("total = ", sum(book.values()))

def main(filename):
    read(filename)


if __name__ == "__main__":
    import sys
    main(sys.argv[1])
