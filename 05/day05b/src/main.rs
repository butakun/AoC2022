use std::io::prelude::*;
use std::io::{BufReader, SeekFrom};
use std::fs::File;

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let filename = &args[1];
    let (mut stacks, moves) = read(filename);

    for (n, from, to) in moves {
        println!("move {n} from {from} to {to}");
        let stack_from = stacks.iter_mut().nth(from - 1).unwrap();
        let mut picked: Vec<char> = stack_from.iter().rev().take(n).cloned().collect();
        stack_from.truncate(stack_from.len() - n);
        let stack_to = stacks.iter_mut().nth(to - 1).unwrap();
        for c in picked.iter().rev().cloned() {
            stack_to.push(c);
        }
        println!("{:?}", stacks);
    }

    let mut code = String::new();
    for stack in stacks {
        code.push(*stack.last().unwrap());
    }
    println!("{code}");
}

fn read(filename: &str) -> (Vec<Vec<char>>, Vec<(usize, usize, usize)>) {
    let f = File::open(filename).unwrap();
    let mut reader = BufReader::new(f);

    let stack_lines: Vec<String> = reader.lines()
        .take_while(|line| { line.as_ref().unwrap().trim().chars().next().unwrap() == '[' })
        .map(|line| { String::from(line.unwrap()) })
        .collect();
    let max_height = stack_lines.len();
    println!("{:?} max = {}", stack_lines, max_height);

    let f = File::open(filename).unwrap();
    reader = BufReader::new(f);
    let line = reader.lines().skip(stack_lines.len()).next().unwrap().unwrap();
    let tokens: Vec<&str> = line.trim().split(" ").filter(|b| b.len() > 0).collect();
    let num_stacks = tokens.len();
    println!("{num_stacks} stacks found");

    let mut stacks: Vec<Vec<char>> = Vec::new();
    for i in 0..num_stacks {
        let mut stack: Vec<char> = Vec::new();
        for j in 0..max_height {
            let l = String::from(&stack_lines[max_height - j - 1]);
            let c = l.chars().nth(1 + 4 * i).unwrap();
            if c.is_alphabetic() {
                stack.push(c);
            }
        }
        println!("stack {i} -> {:?}", stack);
        stacks.push(stack);
    }

    let f = File::open(filename).unwrap();
    reader = BufReader::new(f);
    let moves: Vec<(usize, usize, usize)> = reader.lines()
        .skip(max_height + 1 + 1)
        .map(|line| {
            let line = line.unwrap();
            let tokens: Vec<String> = line.trim().split(" ").map(|s| String::from(s)).collect();
            let n = tokens.iter().nth(1).unwrap().parse::<usize>().unwrap();
            let from = tokens.iter().nth(3).unwrap().parse::<usize>().unwrap();
            let to = tokens.iter().nth(5).unwrap().parse::<usize>().unwrap();
            (n, from, to)
        })
        .collect();

    (stacks, moves)
}
