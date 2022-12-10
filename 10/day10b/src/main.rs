use std::collections::VecDeque;

#[derive(Debug)]
enum Op {
    ADDX(i32),
    NOOP,
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let filename = &args[1];
    let mut ops = read(filename);

    let mut iwait: i32 = 0;
    let mut op = Op::NOOP;
    let mut X: i32 = 1;
    let mut lines: Vec<String> = Vec::new();
    let mut line: String = String::new();
    for i in 1 .. 241 {
        if iwait == 0 {
            match op {
                Op::ADDX(v) => X += v,
                Op::NOOP => (),
            };
            op = match ops.pop_front() {
                Some(o) => o,
                None => break,
            };
            match op {
                Op::ADDX(_) => iwait = 2,
                Op::NOOP => iwait = 1,
            };
        }
        let x = (i - 1) % 40;
        if (x - X).abs() <= 1 {
            line.push('#');
        } else {
            line.push('.');
        }
        if i % 40 == 0 {
            lines.push(line);
            line = String::new();
        }

        println!("{i}, {iwait}, {X}, {:?}", op);
        iwait -= 1;
    }

    for line in lines {
        println!("{line}");
    }
}

fn read(filename: &str) -> VecDeque<Op> {
    std::fs::read_to_string(filename).unwrap()
        .trim()
        .split("\n")
        .map(
            |l| {
                let tokens: Vec<&str> = l.trim().split(" ").collect();
                match tokens[0] {
                    "addx" => Op::ADDX(tokens[1].parse().unwrap()),
                    "noop" => Op::NOOP,
                    _ => panic!("unknown op"),
                }
            }
            )
        .collect()
}
