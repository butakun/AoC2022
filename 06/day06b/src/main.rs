fn main() {
    let args: Vec<String> = std::env::args().collect();
    let filename = &args[1];
    let lines = read(filename);

    for line in lines {
        let count = find_marker(&line);
        println!("{line}: {count}");
    }
}

fn find_marker(line: &str) -> usize {
    let n: usize = 14;
    for (i, c) in line.chars().enumerate() {
        let i0 = std::cmp::max(i as i32 - (n as i32 - 1), 0) as usize;
        let last = &line[i0..i+1];
        let mut distinct = std::collections::HashSet::new();
        for c in last.chars() {
            distinct.insert(c);
        }
        if distinct.len() == n {
            return i + 1;
        }
    }
    0
}

fn read(filename: &str) -> Vec<String> {
    std::fs::read_to_string(filename)
        .unwrap()
        .split("\n")
        .map(|b| String::from(b.trim()))
        .filter(|l| l.len() > 0)
        .collect()
}
