use std::error::Error;
use std::io::prelude::*;
use std::io::BufReader;
use std::fs::File;

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let filename = &args[1];
    let elves = read(filename).unwrap();

    let mut totals: Vec<u32> = Vec::new();
    for elf in elves.iter() {
        let total: u32 = elf.iter().sum();
        totals.push(total);
    }

    let mut indices: Vec<(usize, u32)> = totals.into_iter().enumerate().collect();
    indices.sort_by(|a, b| b.1.cmp(&a.1));

    let mut total: u32 = 0;
    for i in indices.iter().take(3) {
        println!("{:?}", i);
        total += i.1;
    }
    println!("{total}");
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
