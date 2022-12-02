use std::io::prelude::*;
use std::io::BufReader;
use std::fs::File;

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let filename = &args[1];
    let strategies = read(filename);

    let mut total: u32 = 0;
    for strategy in strategies {
        let score = r_p_s(strategy.0, strategy.1);
        total += score;
        println!("{:?} -> {} {}", strategy, score, total);
    }
}

fn r_p_s(opponent: char, me: char) -> u32 {
    match (opponent, me) {
        ('A', 'X') => 1 + 3,
        ('A', 'Y') => 2 + 6,
        ('A', 'Z') => 3 + 0,
        ('B', 'X') => 1 + 0,
        ('B', 'Y') => 2 + 3,
        ('B', 'Z') => 3 + 6,
        ('C', 'X') => 1 + 6,
        ('C', 'Y') => 2 + 0,
        ('C', 'Z') => 3 + 3,
        _ => panic!()
    }
}

fn read(filename: &str) -> Vec<(char, char)> {
    let f = File::open(filename).unwrap();
    let reader = BufReader::new(f);

    reader.lines()
        .map(
            |line| {
                let line = line.unwrap();
                (
                line.chars().nth(0).unwrap(),
                line.chars().nth(2).unwrap()
                )
            }
            )
        .collect()
}
