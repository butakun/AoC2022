use std::collections::VecDeque;

#[derive(Debug, Clone, Copy)]
struct Number {
    lowest_digits: [i32; 9]
}

/*
    const indices: HashMap<i32, usize> =
        HashMap::from([(2, 0), (3, 1), (5, 2), (7, 3), (11, 4), (13, 5), (17, 6), (19, 7), (23, 8)]);
        */

impl Number {
    const bases: [i32; 9] = [2, 3, 5, 7, 11, 13, 17, 19, 23];

    fn new() -> Number {
        Number{ lowest_digits: [0; 9] }
    }

    fn from(value: i32) -> Number {
        let mut num = Number{ lowest_digits: [0; 9] };
        for i in 0 .. Number::bases.len() {
            let base = Number::bases[i];
            num.lowest_digits[i] = value % base;
        }
        num
    }

    fn add(&mut self, value: i32) {
        for i in 0 .. Number::bases.len() {
            let base = Number::bases[i];
            let old = self.lowest_digits[i];
            self.lowest_digits[i] = (old + value) % base;
        }
    }

    fn multiply(&mut self, value: i32) {
        for i in 0 .. Number::bases.len() {
            let base = Number::bases[i];
            let old = self.lowest_digits[i];
            self.lowest_digits[i] = (old * value) % base;
        }
    }

    fn square(&mut self) {
        for i in 0 .. Number::bases.len() {
            let base = Number::bases[i];
            let old = self.lowest_digits[i];
            self.lowest_digits[i] = (old * old) % base;
        }
    }

    fn divisible_by(&self, d: i32) -> bool {
        let i = Number::bases.iter().position(|&x| x == d).unwrap();
        self.lowest_digits[i] == 0
    }
}

#[derive(Debug)]
enum Operation {
    Add(i32),
    Multiply(i32),
    Square,
}

impl Operation {
    fn apply(&self, value: &mut Number) {
        match self {
            Operation::Add(v) => value.add(*v),
            Operation::Multiply(v) => value.multiply(*v),
            Operation::Square => value.square(),
        }
    }
}

#[derive(Debug)]
struct Monkey {
    name: usize,
    items: VecDeque<Number>,
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
            let mut item = match monkey.items.pop_front() {
                Some(v) => v,
                None => break,
            };
            monkey.counted += 1;
            monkey.operation.apply(&mut item);
            let if_true: usize = monkey.if_true;
            let if_false: usize = monkey.if_false;
            if item.divisible_by(monkey.divisor) {
                monkeys[if_true].items.push_back(item);
                //println!("monkey {i}: throws {:?} to monkey {if_true}", item);
            } else {
                monkeys[if_false].items.push_back(item);
                //println!("monkey {i}: throws {:?} to monkey {if_false}", item);
            }
        }
    }
}

fn test() {
    let mut a = Number::from(5);
    println!("{:?}", a);
    a.add(7); // 5 + 7 = 12 = 2 * 2 * 3
    println!("{:?}", a);
    a.multiply(13); // 12  * 13 = 156 = 2 * 2 * 3 * 13
    println!("{:?}", a);
    println!("{:?}", a.divisible_by(13));
    println!("{:?}", a.divisible_by(11));
}

fn main() {
    //test();
    //return;

    let args: Vec<String> = std::env::args().collect();
    let filename = &args[1];

    let mut monkeys = read(filename);
    println!("{:?}", monkeys);

    for i in 0 .. 10000 {
        round(&mut monkeys);
    }
    println!("campaign done");
    println!("{:?}", monkeys);

    let mut counts: Vec<i64> = monkeys.iter().map(|m| m.counted as i64).collect();
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
                            let items: VecDeque<Number> = value.split(",")
                                .map(|t| Number::from(t.trim().parse::<i32>().unwrap()))
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
