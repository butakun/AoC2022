use std::error::Error;
use std::io::prelude::*;
use std::io::BufReader;
use std::fs::File;

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let filename = &args[1];
    let elves = read(filename).unwrap();

    let mut total_cals: Vec<u32> = elves
        .iter()
        .map(|cals| cals.iter().sum())
        .collect();

    total_cals.sort();

    let top_three_sum: u32 = total_cals
        .iter()
        .rev()
        .take(3)
        .sum();
    println!("{top_three_sum}");
}

fn read(filename: &str) -> Result<Vec<Vec<u32>>, Box<dyn Error>> {
    let f = File::open(filename)?;
    let reader = BufReader::new(f);

    let mut elves: Vec<Vec<u32>> = Vec::new();
    let mut items: Vec<u32> = Vec::new();
    for line in reader.lines() {
        let line = line?;
        if line.trim().len() == 0 {
            elves.push(items);
            items = Vec::new();
            continue;
        }
        let calories: u32 = line.parse()?;
        items.push(calories);
    }
    if items.len() > 0 {
        elves.push(items);
    }

    Ok(elves)
}
