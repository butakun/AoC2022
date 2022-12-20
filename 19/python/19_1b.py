import numpy as np


class ActionNode(object):
    """ [ore, clay, obsidian, geode, ore_robot, clay_robot, obsidian_robot, geode_robot, time_remaining] """
    def __init__(self, state):
        self.state = state
    def __hash__(self):
        return hash(self.state.tobytes())
    def __repr__(self):
        return repr(self.state)
    def __str__(self):
        return str(self.state)

class ActionGraph(object):
    def __init__(self, recipe, minutes):
        self.recipe = recipe
        self.minutes = minutes
        self.kinds = ["ore", "clay", "obsidian", "geode"]

        recipe_matrix = np.zeros((len(self.kinds), len(self.kinds)), np.int32)
        for robot, ingredients in self.recipe.items():
            i = self.kinds.index(robot)
            for rock, count in ingredients.items():
                j = self.kinds.index(rock)
                recipe_matrix[i, j] = count
        self.recipe_matrix = recipe_matrix

    def __getitem__(self, u):
        actions = []

        time_remaining = u.state[8]

        if time_remaining > 1:
            for build in [3, 2, 1, 0]:
                if build < 3 and np.all(u.state[4+build] >= self.recipe_matrix[:, build]):
                    # we already have enough robot for making this type
                    #print(f"already have {u.state[4+build]} robots of {self.kinds[build]}, recipe's max is {self.recipe_matrix[:,build]}")
                    continue

                ingredient = self.recipe_matrix[build, :]
                ingredient_mask = ingredient > 0
                can_build = np.all(np.logical_and(u.state[4:8] > 0, ingredient_mask) == ingredient_mask)
                #print(f"we can build {self.kinds[build]} robot")
                if not can_build:
                    continue
                req = np.maximum(ingredient - u.state[0:4], 0)
                req_time = np.ceil(req / np.maximum(u.state[4:8], 1)).astype(np.int32).max()
                if req_time + 1 > time_remaining:
                    continue
                #print(f"{u.state}: req = {req}, wait {req_time} (+1) to build {self.kinds[build]}")
                new_state = u.state.copy()
                new_state[0:4] += u.state[4:8] * (req_time + 1)
                new_state[0:4] -= ingredient
                new_state[4+build] += 1
                new_state[8] -= req_time + 1
                actions.append(ActionNode(new_state))

        if time_remaining > 0:
            new_state = u.state.copy()
            new_state[0:4] += time_remaining * u.state[4:8]
            new_state[8] = 0
            actions.append(ActionNode(new_state))

        return actions


def read(filename):
    with open(filename) as f:
        lines = [ l for l in f ]
    recipes = {}
    robots = set()
    resources = set()
    for line in lines:
        rid, recipe = line.strip().split(":")
        rid = int(rid.split(" ")[1])
        page = [ t.strip() for t in recipe.split(".") if len(t.strip()) > 0 ]
        recipe = {}
        for inst in page:
            robot = inst.split(" ")[1]
            res = inst.split("costs")[1]
            res = [ r.strip() for r in res.split("and") ]
            res = [ r.split(" ") for r in res ]
            res = { v: int(k) for k, v in res }
            recipe[robot] = res
            robots.add(robot)
            resources.update([v for v in res.keys()])
        recipes[rid] = recipe
    return recipes, robots, resources


def test(G):
    initial_state = np.zeros(8 + 1, np.int32)
    initial_state[4] = 1
    initial_state[8] = 24
    initial_state = np.array([2, 1, 1, 0, 1, 1, 1, 0, 24], np.int32)
    actions = G[ActionNode(initial_state)]
    for a in actions:
        print(a)
    return
    for i in range(5):
        print(actions[0])
        actions = G[actions[0]]

def test2(G):
    """
    node = ActionNode(np.array([2, 0, 0, 0, 1, 0, 0, 0, 22], np.int32))
    print(f"From {node}")
    for a in G[node]:
        print(a)

    node = ActionNode(np.array([2, 1, 0, 0, 1, 1, 0, 0, 20], np.int32))
    print(f"From {node}")
    for a in G[node]:
        print(a)

    node = ActionNode(np.array([2, 4, 0, 0, 1, 2, 0, 0, 18], np.int32))
    print(f"From {node}")
    for a in G[node]:
        print(a)

    node = ActionNode(np.array([4, 15, 0, 0, 1, 3, 0, 0, 14], np.int32))
    print(f"From {node}")
    for a in G[node]:
        print(a)
    """

    node = ActionNode(np.array([2, 4, 0, 0, 1, 3, 1, 0, 13], np.int32))
    print(f"From {node}")
    for a in G[node]:
        print(a)


def main(filename):
    recipes, robots, resources = read(filename)
    print(recipes)

    G = ActionGraph(recipes[1], 24)
    print(G.recipe_matrix)

    #test2(G)
    #return

    def visit(G, u, log):
        geode_max = log.get("geode_max",0)
        #print("visiting ", u, geode_max)
        if geode_max < u.state[3]:
            log["geode_max"] = u.state[3]
            print(f"geode max is now {geode_max}")
        for v in G[u]:
            visit(G, v, log)

    quality = 0
    for i, recipe in recipes.items():
        G = ActionGraph(recipes[i], 24)
        initial_state = np.zeros(8 + 1, np.int32)
        initial_state[4] = 1
        initial_state[8] = 24
        log = {"geode_max": 0}
        visit(G, ActionNode(initial_state), log)
        quality += i * log["geode_max"]
        print(log, quality)


if __name__ == "__main__":
    import sys
    main(sys.argv[1])
