use std::io::prelude::*;
use std::io::BufReader;
use std::fs::File;

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let filename = &args[1];

    let sacks = read(filename);
    let mut priorities: u32 = 0;
    for sack in sacks {
        println!("{sack}");
        let prio = to_priorities(&sack);
        println!("prio = {:?}", prio[0]);
        priorities += prio[0];
    }
    println!("priorities sum = {priorities}");
}

fn to_priorities(sack: &str) -> Vec<u32> {
    let items1 = &sack[..sack.len() / 2];
    let items2 = &sack[sack.len() / 2..];

    let mut common_items: Vec<char> = Vec::new();
    for char1 in items1.chars() {
        match items2.find(char1) {
            Some(c) => common_items.push(char1),
            None => ()
        };
    }
    common_items.dedup();
    println!("{:?}", common_items);

    common_items.iter()
        .map(
            |item| match item {
                'a'..='z' => *item as u32 - 'a' as u32 + 1,
                'A'..='Z' => *item as u32 - 'A' as u32 + 27,
                _ => panic!("{item} is invalid")
            }
            )
        .collect()
}

fn read(filename: &str) -> Vec<String> {
    let f = File::open(filename).unwrap();
    let reader = BufReader::new(f);

    reader.lines()
        .map(|line| String::from(line.unwrap().trim()))
        .collect()
}
