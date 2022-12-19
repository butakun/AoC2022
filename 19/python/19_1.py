import re


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


def do_recipe(recipe, robot_names, resource_names):
    robots = { r: 1 if r == "ore" else 0 for r in robot_names }
    resources = { r: 0 for r in resource_names }
    resources["geode"] = 0

    print(robots)
    print(resources)

    for minute in range(10):
        existing_robots = robots.copy()
        while True:
            built_a_robot = False
            for robot, ingredients in recipe.items():
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
    print(robots)
    print(resources)

    do_recipe(recipes[1], robots, resources)

if __name__ == "__main__":
    import sys
    main(sys.argv[1])
