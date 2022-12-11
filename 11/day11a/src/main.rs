use std::collections::VecDeque;

#[derive(Debug)]
enum Operation {
    Add(i32),
    Multiply(i32),
    Square,
}

impl Operation {
    fn apply(&self, value: &mut i32) {
        match self {
            Operation::Add(v) => *value = *value + v,
            Operation::Multiply(v) => *value = *value * v,
            Operation::Square => *value = *value * *value,
        }
    }
}

#[derive(Debug)]
struct Monkey {
    name: usize,
    items: VecDeque<i32>,
    operation: Operation,
    divisor: i32,
    if_true: usize,
    if_false: usize,
    counted: i32,
}

impl Monkey {
    fn new() -> Monkey {
        Monkey{
            name: 0,
            items: VecDeque::new(),
            operation: Operation::Add(0),
            divisor: 1,
            if_true: 0,
            if_false: 0,
            counted: 0,
        }
    }
}

fn round(monkeys: &mut Vec<Monkey>) {
    for i in 0 .. monkeys.len() {
        loop {
            let monkey = &mut monkeys[i];
            let mut item = match  monkey.items.pop_front() {
                Some(v) => v,
                None => break,
            };
            monkey.counted += 1;
            monkey.operation.apply(&mut item);
            item = item / 3;
            let if_true: usize = monkey.if_true;
            let if_false: usize = monkey.if_false;
            if item % monkey.divisor == 0 {
                monkeys[if_true].items.push_back(item);
                println!("monkey {i}: throws {item} to monkey {if_true}");
            } else {
                monkeys[if_false].items.push_back(item);
                println!("monkey {i}: throws {item} to monkey {if_false}");
            }
        }
    }
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let filename = &args[1];

    let mut monkeys = read(filename);
    println!("{:?}", monkeys);

    for i in 0 .. 20 {
        round(&mut monkeys);
    }
    println!("campaign done");
    println!("{:?}", monkeys);

    let mut counts: Vec<i32> = monkeys.iter().map(|m| m.counted).collect();
    counts.sort();
    counts.reverse();
    let res = counts[0] * counts[1];
    println!("{:?} -> {res}", counts);
}

fn read(filename: &str) -> Vec<Monkey> {
    std::fs::read_to_string(filename)
        .unwrap()
        .trim()
        .split("\n\n")
        .map(
            |lines| {  // for a monkey
                lines.trim()
                    .split("\n")
                    .map(
                        |l| {
                            let tokens: Vec<&str> = l.trim().split(":")
                                .map(|t| t.trim())
                                .collect();
                            (tokens[0].to_string(), tokens[1].to_string())
                        }
                        )
                    .collect()
            }
            )
        .map(
            |dict: Vec<(String, String)>| {
                let mut monkey = Monkey::new();
                for (key, value) in dict {
                    match key.as_str() {
                        s if key.starts_with("Monkey") => {
                            let tokens: Vec<&str> = s.split(" ").collect();
                            monkey.name = tokens[1].parse().unwrap();
                        },
                        "Starting items" => {
                            let items: VecDeque<i32> = value.split(",")
                                .map(|t| t.trim().parse::<i32>().unwrap())
                                .collect();
                            monkey.items = items;
                        },
                        "Operation" => {
                            let exp: Vec<&str> = value.split(" ").collect();
                            match exp[3] {
                                "+" => {
                                    let value = exp[4].parse::<i32>().unwrap();
                                    monkey.operation = Operation::Add(value);
                                },
                                "*" => {
                                    if exp[4] == "old" {
                                        monkey.operation = Operation::Square;
                                    } else {
                                        let value = exp[4].parse::<i32>().unwrap();
                                        monkey.operation = Operation::Multiply(value);
                                    }
                                },
                                _ => {
                                    panic!("invalid expression");
                                }
                            }
                        },
                        "Test" => {
                            let tokens: Vec<&str> = value.split(" ").collect();
                            let divisor = tokens[2].parse::<i32>().unwrap();
                            monkey.divisor = divisor;
                        },
                        "If true" => {
                            let tokens: Vec<&str> = value.split(" ").collect();
                            let to = tokens[3].parse::<usize>().unwrap();
                            monkey.if_true = to;
                        },
                        "If false" => {
                            let tokens: Vec<&str> = value.split(" ").collect();
                            let to = tokens[3].parse::<usize>().unwrap();
                            monkey.if_false = to;
                        },
                        s => {
                            println!("key '{s}'");
                        },
                    };
                }
                monkey
            }
            )
        .collect()
}
