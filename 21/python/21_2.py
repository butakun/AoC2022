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


def test1(g):
    print(g(1e12))
    print(g(5e11))
    print(g(1e10))

def test2(f):
    v0 = 5e11
    for i in range(100000):
        v = v0 + 1e6 * i
        f1, f2 = f(v)
        print(v, f1, f2, f1 - f2)
    return

def main(filename):
    tree = read(filename)
    print(tree)

    def visit(tree, node):
        data, children = tree[node]
        if not children:
            if node == "humn":
                return lambda v: v
            else:
                return lambda v: data
        f1 = visit(tree, children[0])
        f2 = visit(tree, children[1])
        if node == "root":
            return lambda v: (f1(v), f2(v))
        else:
            if data == "+":
                return lambda v: f1(v) + f2(v)
            elif data == "-":
                return lambda v: f1(v) - f2(v)
            elif data == "*":
                return lambda v: f1(v) * f2(v)
            elif data == "/":
                return lambda v: f1(v) / f2(v)

    f = visit(tree, "root")
    def g(v):
        v1, v2 = f(v)
        return v1 - v2

    x1 = 1000
    x2 = 2 * x1
    g1 = g(x1)
    g2 = g(x2)
    print("initial guess for Newton Method (damped secant method) = ", x1, x2, g1, g2)
    coef = 1e-2
    for i in range(10000):
        dx = - (g2 -g1) / (x2 - x1) * g2
        if abs(dx) < 1.0:
            break
        x3 = x2 + coef * dx
        g3 = g(x3)
        print("x3 = ", x3, g3)
        x1 = x2
        x2 = x3
        g1 = g2
        g2 = g3

    answer = int(round(x2))
    v1, v2 = f(answer)
    print(answer, v1, v2)

if __name__ == "__main__":
    import sys
    main(sys.argv[1])
