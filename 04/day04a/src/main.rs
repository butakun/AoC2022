use std::io::prelude::*;
use std::io::BufReader;
use std::fs::File;

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let filename = &args[1];
    let pairs = read(filename);
    println!("{:?}", pairs);

    let mut count: u32 = 0;
    for pair in pairs {
        if overlaps(&pair.0, &pair.1) {
            count += 1;
            println!("{:?} and {:?} overlaps", pair.0, pair.1);
        }
    }
    println!("{count} pairs overlap");
}

fn overlaps(pair1: &(u32, u32), pair2: &(u32, u32)) -> bool {
    (pair1.0 <= pair2.0 && pair2.1 <= pair1.1) ||
    (pair2.0 <= pair1.0 && pair1.1 <= pair2.1)

}

fn read(filename: &str) -> Vec<((u32, u32), (u32, u32))> {
    let f = File::open(filename).expect("couldn't open file");
    let reader = BufReader::new(f);

    reader.lines()
        .map(|line| {
            let pair: Vec<(u32, u32)> =
            line.unwrap()
                .split(',')
                .map(|range| {
                    let r: Vec<&str> = range.split('-').collect();
                    (r[0].parse().unwrap(), r[1].parse().unwrap())
                })
                .collect();
            (pair[0], pair[1])
        })
        .collect()
}
