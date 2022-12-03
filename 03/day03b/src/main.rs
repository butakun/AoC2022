use std::io::prelude::*;
use std::io::BufReader;
use std::fs::File;

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let filename = &args[1];

    let groups = read(filename);

    let mut total: u32 = 0;
    for group in groups {
        let c = find_common_item(&group).unwrap();
        let prio = to_priority(c);
        println!("{:?} -> {c} {prio}", group);
        total += prio;
    }
    println!("total = {total}");
}

fn to_priority(item: char) -> u32 {
    match item {
        'a'..='z' => item as u32 - 'a' as u32 + 1,
        'A'..='Z' => item as u32 - 'A' as u32 + 27,
        _ => panic!("{item} is invalid")
    }
}

fn find_common_item(group: &Vec<String>) -> Option<char> {
    for c1 in group[0].chars() {
        match group[1].find(c1) {
            Some(c) => {
                match group[2].find(c1) {
                    Some(c) => return Some(c1),
                    None => ()
                }
            },
            None => ()
        }
    }
    None
}

fn read(filename: &str) -> Vec<Vec<String>> {
    let f = File::open(filename).unwrap();
    let reader = BufReader::new(f);

    let sacks: Vec<String> =
        reader.lines()
        .map(|line| String::from(line.unwrap().trim()))
        .collect();

    let mut groups: Vec<Vec<String>> = Vec::new();
    let mut iter = sacks.iter().peekable();
    while iter.peek().is_some() {
        let mut group: Vec<String> = Vec::new();
        group.push(iter.next().unwrap().to_string());
        group.push(iter.next().unwrap().to_string());
        group.push(iter.next().unwrap().to_string());
        groups.push(group);
    }
    groups
}
