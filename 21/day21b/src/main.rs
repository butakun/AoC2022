use std::collections::HashMap;

#[derive(Debug)]
enum FuncNode {
    Number(i64),
    Op(String, char, String),
}

impl FuncNode {
    fn call(&self, tree: &HashMap<String, FuncNode>, value: i64) -> Fn {
        match self {
            FuncNode::Number(v) => move |value| v,
            FuncNode::Op(name1, op, name2) => move |value| self._op(tree, name1, *op, name2, value),
        }
    }

    fn _op(&self, tree: &HashMap<String, FuncNode>, name1: &str, op: char, name2: &str, value: i64) -> Fn {
        let v1 = tree[name1].call(tree, value);
        let v2 = tree[name2].call(tree, value);
        match op {
            '+' => move |value| v1 + v2,
            '-' => move |value| v1 - v2,
            '*' => move |value| v1 * v2,
            '/' => move |value| v1 / v2,
            _ => panic!("unknown op"),
        }
    }
}

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
    //let answer = visit(&tree, &tree["root"]);
    //println!("{answer}");
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

fn read(filename: &str) -> HashMap<String, FuncNode> {
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
                    FuncNode::Number(tokens[0].parse::<i64>().unwrap())
                    ),
                3 => (
                    n.0.clone(),
                    FuncNode::Op(
                        tokens[0].to_string(),
                        tokens[1].chars().next().unwrap(),
                        tokens[2].to_string()
                        )
                    ),
                _ => panic!()
            }
        })
        .collect::<HashMap<String, FuncNode>>()
}
