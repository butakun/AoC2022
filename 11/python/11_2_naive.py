from pprint import pprint


class Operation(object):
    def __init__(self, exp):
        self._exp = exp
    def __call__(self, old):
        return eval(self._exp, {}, {"old": old})


def read(filename):
    monkeys = []
    monkey = {}
    for line in open(filename):
        line = line.strip()
        if "Name" not in monkey:
            monkey["Name"] = line.split(":")[0]
        elif len(line) > 0:
            key, value = line.split(":")
            value = value.strip()
            monkey[key] = value
        else:
            monkeys.append(monkey)
            monkey = {}
    if monkey:
        monkeys.append(monkey)

    for monkey in monkeys:
        name = monkey["Name"].strip().split(" ")[-1]
        monkey["Name"] = int(name)

        ms = [int(v) for v in monkey["Starting items"].split(",")]
        monkey["Starting items"] = ms

        ops = monkey["Operation"].split("=")
        assert ops[0].strip() == "new"
        expression = ops[1].strip()
        print("expression = ", expression)
        monkey["Operation"] = Operation(expression)

        test = monkey["Test"].strip().split(" ")
        assert test[0] == "divisible" and test[1] == "by"
        monkey["Test"] = "divisible by", int(test[2])

        for k in ["If true", "If false"]:
            to = monkey[k].strip()
            assert to.startswith("throw to")
            to = int(to.split(" ")[-1])
            monkey[k] = to

        monkey["Counted"] = 0

    return monkeys


def round(monkeys):
    print("### round begins")
    for m in monkeys:
        items = m["Starting items"]
        while items:
            item = items.pop(0)
            item = m["Operation"](item)
            #item = int(item / 3)
            recv_true  = monkeys[m["If true"]]
            recv_false = monkeys[m["If false"]]
            test = item % m["Test"][1] == 0
            if test:
                assert recv_true["Name"] == m["If true"]
                recv_true["Starting items"].append(item)
            else:
                assert recv_false["Name"] == m["If false"]
                recv_false["Starting items"].append(item)
            m["Counted"] += 1

        print(f"*** after {m['Name']} is done")
        pprint(monkeys)

    print("### round done")
    pprint(monkeys)

def main(filename):
    monkeys = read(filename)

    for i in range(10000):
        round(monkeys)

    print("campaign done")
    pprint(monkeys)

    counts = [ m["Counted"] for m in monkeys ]
    counts.sort(reverse=True)
    print(counts)
    print(counts[0] * counts[1])


if __name__ == "__main__":
    import sys
    main(sys.argv[1])
