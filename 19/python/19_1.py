import numpy as np


class ActionNode(object):
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

        # where you build one kind of robot
        build = [False] * 4
        skip_no_build = False
        for kind in [3, 2, 1, 0]:
            ingredient = self.recipe_matrix[kind, :]
            if np.all(u.state[:4] >= ingredient):
                build[kind] = True
            elif kind < 3 and np.all(u.state[4 + kind] >= self.recipe_matrix[:, kind]):
                #print(f"no point building {kind} because {u.state[4+kind]} >= {self.recipe_matrix[:, kind]}")
                build[kind] = False
            else:
                pass

        if u.state[8] > 1:
            for kind in [3, 2, 1, 0]:
                if not build[kind]:
                    continue
                next_state = u.state.copy()
                next_state[:4] -= self.recipe_matrix[kind, :]
                next_state[4+kind] += 1
                next_state[:4] += u.state[4:8]
                next_state[8] -= 1
                actions.append(ActionNode(next_state))

        # where you don't build anything, just collect rocks
        if True or not skip_no_build:
            next_state = u.state.copy()
            next_state[:4] += u.state[4:8]
            next_state[8] -= 1
            actions.append(ActionNode(next_state))

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


def do_recipe(recipe, robot_names, resource_names, minutes):
    robots = { r: 1 if r == "ore" else 0 for r in robot_names }
    resources = { r: 0 for r in resource_names }
    resources["geode"] = 0

    for minute in range(minutes):
        existing_robots = robots.copy()
        while True:
            built_a_robot = False
            #for robot, ingredients in recipe.items():
            for robot in ["geode", "obsidian", "clay", "ore"]:
                ingredients = recipe[robot]
                can_build = True
                for rock, count in ingredients.items():
                    if resources[rock] < count:
                        can_build = False
                        break
                if can_build:
                    for rock, count in ingredients.items():
                        resources[rock] -= count
                    robots[robot] += 1
                    built_a_robot = True
                    print(f"  made {robot} robot from ",  ", ".join([ f"{count} {rock}(s)" for rock, count in ingredients.items() ]))
            if not built_a_robot:
                break
        for robot, count in existing_robots.items():
            print(f"  {robot} robot collecting {count} {robot}(s)")
            resources[robot] += count
        
        print(f"after minute {minute+1}: res = {resources}, robots = {robots}")

def main(filename):
    recipes, robots, resources = read(filename)
    print(recipes)
    #print(robots)
    #print(resources)

    #do_recipe(recipes[1], robots, resources, 24)

    G = ActionGraph(recipes[1], 24)
    print(G.recipe_matrix)

    initial_state = np.zeros(8 + 4, np.int32)
    initial_state[4] = 1
    initial_state[8] = 24
    actions = G[ActionNode(initial_state)]
    for a in actions:
        print(a)
    actions = G[actions[0]]
    for a in actions:
        print(a)

    def visit(G, u, minute, log):
        geode_max = log.get("geode_max",0)
        print("visiting ", u, minute, geode_max)
        log["geode_max"] = max(geode_max, u.state[3])
        if minute <= 0:
            return
        for v in G[u]:
            visit(G, v, minute - 1, log)
    log = {}
    visit(G, ActionNode(initial_state), 24, log)
    print(log)


if __name__ == "__main__":
    import sys
    main(sys.argv[1])
