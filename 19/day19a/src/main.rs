use std::collections::HashMap;

#[derive(Debug, Clone, Copy)]
struct Node {
    state: [i32; 8],
    minutes_remaining: i32,
}

impl Node {
    fn from(state: [i32; 8], minutes_remaining: i32) -> Node {
        Node {
            state: state,
            minutes_remaining: minutes_remaining,
        }
    }
}

#[derive(Debug)]
struct Graph {
    recipe_matrix: [[i32; 4]; 4],
    kinds: HashMap<String, usize>
}

impl Graph {
    fn from(recipe: &HashMap<String, HashMap<String, i32>>) -> Graph {
        let mut G = Graph{
            recipe_matrix: [[0; 4]; 4],
            kinds: HashMap::from([
                                 ("ore".to_string(), 0),
                                 ("clay".to_string(), 1),
                                 ("obsidian".to_string(), 2),
                                 ("geode".to_string(), 3),
            ]),
        };
        for (robot, ingredients) in recipe.iter() {
            let i = G.kinds[robot];
            for (rock, count) in ingredients.iter() {
                let j = G.kinds[rock];
                G.recipe_matrix[i][j] = *count;
            }
        }
        G
    }

    fn neighbors(node: &Node) -> Vec<Node> {
        let mut actions = Vec::<Node>::new();
        let mut node = node.clone();
        node.minutes_remaining -= 1;
        actions.push(node);
        actions
    }
}

fn main() {
    let filename = std::env::args().skip(1).next().unwrap();
    let recipes = read(&filename);

    println!("{0:?}", recipes.get(&1));

    let G = Graph::from(&recipes[&1]);
    println!("{G:?}");
}

fn read(filename: &str) -> HashMap<i32, HashMap<String, HashMap<String, i32>>> {
    std::fs::read_to_string(filename).unwrap()
        .trim()
        .split("\n")
        .map(
            |line| {
                line.split_once(':')
                    .map(
                        |split| {
                            (
                                split.0.split_once(' ').unwrap().1
                                .parse::<i32>().unwrap(),
                                split.1.split('.')
                                .filter(|s| !s.is_empty())
                                .map(
                                    |s| {
                                        let tokens
                                            = s.trim().split_once("costs").unwrap();
                                        (
                                            tokens.0.split(' ').skip(1).next().unwrap().to_string(),
                                            tokens.1.split("and")
                                                .map(
                                                    |s| {
                                                        let tokens = s.trim().split_once(' ').unwrap();
                                                        (
                                                            tokens.1.trim().to_string(),
                                                            tokens.0.trim().parse::<i32>().unwrap()
                                                            )

                                                    }
                                                    )
                                                .collect::<HashMap<String, i32>>()
                                            )
                                    }
                                    )
                                .collect::<HashMap<String, HashMap<String, i32>>>()
                                )
                        }
                        )
                    .unwrap()
            }
            )
        .collect::<HashMap<i32, HashMap<String, HashMap<String, i32>>>>()
}
