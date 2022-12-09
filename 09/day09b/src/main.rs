use std::ops::{Add, Sub};
use std::collections::HashSet;
use std::fmt;

#[derive(Debug, Copy, Clone, PartialEq, Eq, Hash)]
struct Pos {
    x: i32,
    y: i32,
}

impl Add for Pos {
    type Output = Pos;
    fn add(self, other: Self) -> Pos {
        Pos { x: self.x + other.x, y: self.y + other.y }
    }
}

impl<'a, 'b> Add<&'b Pos> for &'a Pos {
    type Output = Pos;
    fn add(self, other: &'b Pos) -> Pos {
        Pos { x: self.x + other.x, y: self.y + other.y }
    }
}

impl Sub for Pos {
    type Output = Pos;
    fn sub(self, other: Self) -> Pos {
        Pos { x: self.x - other.x, y: self.y - other.y }
    }
}

impl<'a, 'b> Sub<&'b Pos> for &'a Pos {
    type Output = Pos;
    fn sub(self, other: &'b Pos) -> Pos {
        Pos { x: self.x - other.x, y: self.y - other.y }
    }
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let filename = &args[1];
    let moves = read(filename);
    println!("{:?}", moves);

    let mut HH: [Pos; 10] = [Pos{x: 0, y: 0}; 10];
    let mut visited = HashSet::<Pos>::new();
    visited.insert(HH[HH.len()-1]);

    for (direction, steps) in moves {
        let dH = match direction {
            'U' => Pos{x: 0, y: -1},
            'D' => Pos{x: 0, y: 1},
            'L' => Pos{x: -1, y: 0},
            'R' => Pos{x: 1, y: 0},
            _ => panic!("wtf do you mean by {direction}"),
        };

        for step in 0..steps {
            HH[0] = HH[0] + dH;
            for i in 0 .. HH.len()-1 {
                let H = HH[i];
                let h = &mut HH[i + 1];
                let dh = move_tail(&H, h);
                *h = *h + dh;
            }
            visited.insert(HH[HH.len()-1]);
            println!("{:?}", HH);
        }
    }
    println!("visited {}", visited.len());
}

fn move_tail(H: &Pos, T: &Pos) -> Pos {
    let d = H - T;
    if d.x.abs() <= 1 && d.y.abs() <= 1 {
        Pos{x: 0, y: 0}
    } else if d.x == 0 {
        Pos{x: 0, y: d.y / d.y.abs()}
    } else if d.y == 0 {
        Pos{x: d.x / d.x.abs(), y: 0}
    } else {
        Pos{x: d.x / d.x.abs(), y: d.y / d.y.abs()}
    }
}

fn read(filename: &str) -> Vec<(char, i32)> {
    std::fs::read_to_string(filename)
        .unwrap()
        .trim()
        .split("\n")
        .map(
            |l| {
                let tokens: Vec<&str> = l.split(" ").collect();
                (tokens[0].chars().next().unwrap(), tokens[1].parse::<i32>().unwrap())
            })
        .collect()
}
