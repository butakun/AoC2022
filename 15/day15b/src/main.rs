use std::collections::{HashMap, HashSet, VecDeque};
use rand::thread_rng;
use rand::seq::SliceRandom;

fn main() {
    let filename = std::env::args().skip(1).next().unwrap();
    let measured = read(&filename);
    println!("{measured:?}");

    let mut ilines: Vec<i32> = (0 .. 4000000).collect();
    ilines.shuffle(&mut thread_rng());

    //for iline in 0 ..= 4000000 {
    for iline in ilines {
        let ranges = check_line(&measured, iline);
        if ranges.len() > 1 {
            let ihole = ranges[0].1 + 1;
            let freq = (ihole as u64) * 4000000 + iline as u64;
            println!("({ihole}, {iline}) freq = {freq}");
            break;
        }
    }
}

fn check_line(measured: &Vec<((i32, i32), (i32, i32), i32)>, check_line: i32) -> Vec<(i32, i32)> {
    let mut ranges: Vec<(i32, i32)> = vec![];

    for (sensor, beacon, dist) in measured {
        let dist_to_check_line = (check_line - sensor.1).abs();
        if dist_to_check_line > *dist {
            continue;
        }

        let width = dist - dist_to_check_line;
        let i = sensor.0;
        let range = (i - width, i + width);
        ranges.push(range);
    }

    union(&ranges)
}

fn union(ranges: &Vec<(i32, i32)>) -> Vec<(i32, i32)> {
    let n = ranges.len();
    let mut graph: HashMap<usize, Vec<usize>> = HashMap::new();

    for i1 in 0 .. n {
        let r1 = ranges[i1];
        for i2 in i1+1 .. n {
            let r2 = ranges[i2];
            if overlaps(&r1, &r2) {
                //println!("{i1}:{r1:?} and {i2}:{r2:?} overlaps");
                graph.entry(i1).or_insert(Vec::new()).push(i2);
                graph.entry(i2).or_insert(Vec::new()).push(i1);
            }
        }
    }

    let mut groups: Vec<HashSet<usize>> = Vec::new();
    let mut grouped: HashSet<usize> = HashSet::new();
    for i in 0 .. n {
        if grouped.contains(&i) {
            continue;
        }
        let group = connected_component(&graph, i);
        grouped.extend(&group);
        groups.push(group);
    }

    let mut fused_ranges: Vec<(i32, i32)> = Vec::new();
    for group in groups {
        let mut imin: Option<i32> = None;
        let mut imax: Option<i32> = None;
        for l in group {
            if let Some(i) = imin {
                imin = Some(std::cmp::min(ranges[l].0, i));
            } else {
                imin = Some(ranges[l].0);
            }
            if let Some(i) = imax {
                imax = Some(std::cmp::max(ranges[l].1, i));
            } else {
                imax = Some(ranges[l].1);
            }
        }
        let imin = imin.unwrap();
        let imax = imax.unwrap();
        fused_ranges.push((imin, imax));
    }

    fused_ranges
}

fn overlaps(r1: &(i32, i32), r2: &(i32, i32)) -> bool {
    (r1.0 - 1) <= r2.1 && r2.0 <= (r1.1 + 1)
}

fn connected_component(G: &HashMap<usize, Vec<usize>>, start: usize) -> HashSet<usize> {
    let mut visited: HashSet<usize> = HashSet::new();
    let mut Q: VecDeque<usize> = VecDeque::from([start]);
    
    while ! Q.is_empty() {
        let u = Q.pop_front().unwrap();
        for v in G.get(&u).unwrap() {
            if ! visited.contains(v) {
                Q.push_back(*v);
                visited.insert(*v);
            }
        }
    }
    visited
}

fn read(filename: &str) -> Vec<((i32, i32), (i32, i32), i32)> {
    std::fs::read_to_string(filename).unwrap()
        .trim()
        .split("\n")
        .map(|line| {
            let tokens: Vec<&str> = line.split(" ").collect();
            let xs = tokens[2].split_once("=").unwrap().1.split_once(",").unwrap().0.parse::<i32>().unwrap();
            let ys = tokens[3].split_once("=").unwrap().1.split_once(":").unwrap().0.parse::<i32>().unwrap();
            let xb = tokens[8].split_once("=").unwrap().1.split_once(",").unwrap().0.parse::<i32>().unwrap();
            let yb = tokens[9].split_once("=").unwrap().1.parse::<i32>().unwrap();
            let d = (xb - xs).abs() + (yb - ys).abs();
            ((xs, ys), (xb, yb), d)
        })
        .collect()
}
