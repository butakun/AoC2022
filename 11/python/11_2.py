from pprint import pprint
from number import Number


class Number(object):
    """ we only keep track of the digits in radix-N represetation
    where N is one of the following"""
    divisors = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    indices = { d: i for i, d in enumerate(divisors) }

    def __init__(self, value):
        self._reminders = [ value % d for d in Number.divisors ]

    def add(self, v):
        for i, d in enumerate(Number.divisors):
            r = (self._reminders[i] + v) % d
            self._reminders[i] = r

    def multiply(self, v):
        for i, d in enumerate(Number.divisors):
            p = (self._reminders[i] * v) % d
            self._reminders[i] = p

    def square(self):
        for i, d in enumerate(Number.divisors):
            s = (self._reminders[i] * self._reminders[i]) % d
            self._reminders[i] = s

    def divisible_by(self, d):
        assert d in Number.divisors, f"divisor {d} not found in {Number.divisors}"
        return self._reminders[Number.indices[d]] == 0

    def __repr__(self):
        return f"{self._reminders}"


class Operation(object):
    def __init__(self, exp):
        ops = exp.split(" ")
        op = ops[1]
        value = ops[2]
        assert op == "*" or op == "+", f"op was {op}"
        if ops[2] == "old":
            assert op == "*"
            op = "^"
            value = None
        else:
            value = int(value)
        self._op = op
        self._value = value

    def __call__(self, old):
        if self._op == "*":
            old.multiply(self._value)
        elif self._op == "+":
            old.add(self._value)
        elif self._op == "^":
            old.square()
        else:
            raise ValueError(f"op {self._op} invalid")


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

        ms = [Number(int(v)) for v in monkey["Starting items"].split(",")]
        monkey["Starting items"] = ms

        ops = monkey["Operation"].split("=")
        expression = ops[1].strip()
        print(f"expression = '{expression}'")

        test = monkey["Test"].strip().split(" ")
        divisor = int(test[2])
        monkey["Divisor"] = divisor

        monkey["Operation"] = Operation(expression)

        for k in ["If true", "If false"]:
            to = monkey[k].strip()
            to = int(to.split(" ")[-1])
            monkey[k] = to

        monkey["Counted"] = 0

    return monkeys


def round(monkeys):
    for m in monkeys:
        items = m["Starting items"]
        while items:
            item = items.pop(0)
            m["Operation"](item)
            recv_true  = monkeys[m["If true"]]
            recv_false = monkeys[m["If false"]]
            test = item.divisible_by(m["Divisor"])
            if test:
                recv_true["Starting items"].append(item)
            else:
                recv_false["Starting items"].append(item)
            m["Counted"] += 1


def main(filename):
    monkeys = read(filename)

    for i in range(10000):
        round(monkeys)
        if i % 100 == 0:
            print(f"round {i} done")

    print("campaign done")
    pprint(monkeys)

    counts = [ m["Counted"] for m in monkeys ]
    counts.sort(reverse=True)
    print(counts)
    print(counts[0] * counts[1])


if __name__ == "__main__":
    import sys
    main(sys.argv[1])
