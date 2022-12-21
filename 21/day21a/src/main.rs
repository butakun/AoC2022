use std::collections::HashMap;

#[derive(Debug)]
struct Node {
    name: String,
    value: Option<i64>,
    child1: Option<String>,
    child2: Option<String>,
    op: char,
}

fn main() {
    let filename = std::env::args().skip(1).next().unwrap();
    let tree = read(&filename);

    println!("{tree:?}");
    let answer = visit(&tree, &tree["root"]);
    println!("{answer}");
}

fn visit(tree: &HashMap<String, Node>, u: &Node) -> i64 {
    match u.value {
        Some(value) => value,
        None => {
            let v1 = match &u.child1 {
                Some(name) => visit(tree, &tree[name]),
                None => panic!(),
            };
            let v2 = match &u.child2 {
                Some(name) => visit(tree, &tree[name]),
                None => panic!(),
            };
            match u.op {
                '+' => v1 + v2,
                '-' => v1 - v2,
                '*' => v1 * v2,
                '/' => v1 / v2,
                _ => panic!(),
            }
        }
    }
}

fn read(filename: &str) -> HashMap<String, Node> {
    std::fs::read_to_string(filename).unwrap()
        .trim()
        .split('\n')
        .map(|l| l.split_once(": ").unwrap())
        .map(|t| (t.0.to_string(), t.1.to_string()))
        .map(|n| {
            let tokens = n.1.split(' ').collect::<Vec<&str>>();
            match tokens.len() {
                1 => (
                    n.0.clone(),
                    Node{ name: n.0, value: Some(tokens[0].parse::<i64>().unwrap()), child1: None, child2: None, op: ' ' }
                    ),
                3 => (
                    n.0.clone(),
                    Node{
                        name: n.0, value: None,
                        child1: Some(tokens[0].to_string()), child2: Some(tokens[2].to_string()),
                        op: tokens[1].chars().next().unwrap()
                    }
                    ),
                _ => panic!()
            }
        })
        .collect::<HashMap<String, Node>>()
}
