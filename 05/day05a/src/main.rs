use std::io::prelude::*;
use std::io::{BufReader, SeekFrom};
use std::fs::File;

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let filename = &args[1];
    let (mut stacks, moves) = read(filename);

    let ops = moves.len();

    for (count, (n, from, to)) in moves.into_iter().enumerate() {
        for i in 0..n {
            let stack_from = stacks.iter_mut().nth(from-1).unwrap();
            let c = stack_from.pop().unwrap();
            let stack_to = stacks.iter_mut().nth(to-1).unwrap();
            stack_to.push(c);
        }
        //let buf: Vec<String> = stacks.iter().map(|stack| stack.into_iter().collect()).collect();
        //let vis = visual(stacks, n, from, to);
        //println!("moved {n} from {from} to {to}: {:?}", buf);
        if count % 1000 == 0 {
            println!("{count} / {ops}: moved {n} from {from} to {to}");
        }
    }

    let mut code = String::new();
    for stack in stacks {
        code.push(*stack.last().unwrap());
    }
    println!("{code}");
}

/*
fn visual(stacks: &Vec<Vec<char>>, n: usize, from: usize, to: usize) -> String {
    let buf = stacks.iter()
        .enumerate()
        .map(|(i, stack)| {
            match i {
                to => {
                    let mut b = String::new();
                    write!(b, "[{}]", stack.into_},
                _ => stack.into_iter().collect()
}
*/

fn read(filename: &str) -> (Vec<Vec<char>>, Vec<(usize, usize, usize)>) {
    let f = File::open(filename).unwrap();
    let mut reader = BufReader::new(f);

    let stack_lines: Vec<String>;
    let mut stack_ids: Vec<usize> = Vec::new();
    stack_lines = reader.by_ref().lines()
        .take_while(|line| {
            let line = line.as_ref().unwrap();
            let c = line.trim().chars().next().unwrap();
            if c == '[' {
                true
            } else {
                stack_ids = line.trim()
                    .split(" ")
                    .filter(|b| b.len() > 0)
                    .map(|b| b.parse().unwrap())
                    .collect();
                false
            }
        })
        .map(|line| String::from(line.unwrap()))
        .collect();

    let max_height = stack_lines.len();

    let mut stacks: Vec<Vec<char>> = Vec::new();
    for stack_id in stack_ids {
        stacks.push(Vec::new());
    }

    for (i, stack) in stacks.iter_mut().enumerate() {
        for j in 0..max_height {
            let l = &stack_lines[max_height - j - 1];
            let c = l.chars().nth(1 + 4 * i).unwrap();
            if c.is_alphabetic() {
                stack.push(c);
            }
        }
    }

    let moves: Vec<(usize, usize, usize)> = reader.by_ref().lines().skip(1)
        .map(|line| {
            let line = line.unwrap();
            let tokens: Vec<String> = line.trim().split(" ")
                .map(|s| String::from(s))
                .collect();
            let n: usize = tokens.iter().nth(1).unwrap().parse().unwrap();
            let from: usize = tokens.iter().nth(3).unwrap().parse().unwrap();
            let to: usize = tokens.iter().nth(5).unwrap().parse().unwrap();
            (n, from, to)
        })
        .collect();

    (stacks, moves)
}
