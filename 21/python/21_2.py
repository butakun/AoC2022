from collections import deque


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


def newton(g, x1, x2, coef, debug=False):
    g1 = g(x1)
    g2 = g(x2)
    print(f"initial guess for Newton-Raphson iterations with underrelaxation with coef = {coef} = ", x1, x2, g1, g2)
    for i in range(1000):
        dx = - (g2 -g1) / (x2 - x1) * g2
        x3 = x2 + coef * dx
        g3 = g(x3)
        if debug:
            print(f"Iteration {i}: x3 = {x3}, g3 = {g3}")
        if abs(g3) < 0.1:
            break

        x1 = x2
        x2 = x3
        g1 = g2
        g2 = g3
    answer = int(round(x3))
    return answer, i


def main(filename):
    tree = read(filename)

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

    coef = 1e-2
    x1 = 1000
    x2 = 2 * x1

    for trial in range(100):
        try:
            answer, iters = newton(g, x1, x2, coef)
            v1, v2 = f(answer)
            v1, v2 = int(v1), int(v2)
            if v1 != v2:
                raise ValueError
            print(f"answer = {answer} after {iters} iterations, {v1} == {v2}? {v1==v2}")
            break
        except:
            coef *= 0.5

if __name__ == "__main__":
    import sys
    main(sys.argv[1])
