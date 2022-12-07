use std::collections::HashMap;

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let filename = &args[1];
    let fs = read(filename);

    println!("{:?}", fs);
}

struct FileSystem {
    entries: HashMap<u32, Entry>,
    next_inode: u32
}

impl FileSystem {
    fn new() -> Self {
        Self { entries: HashMap::new(), next_inode: 0 }
    }
}

#[derive(Debug)]
enum Entry {
    File { name: String, next: Option<u32> },
    Dir { name: String, next: Option<u32>, target: Option<u32>, last: Option<u32> },
}

fn append_entry_to_node(fs: &mut FileSystem, inode: u32, entry: Entry) {
    let mut node = fs.entries.get(&inode).unwrap();
    match node {
        Entry::Dir{ name, next, target, last } => {
            let new_inode = fs.next_inode;
            fs.next_inode += 1;
            if let Some(l) == last {
                fs.entries.insert(new_inode, entry);
                if let Entry::
                fs.entries.get(l).unwrap().next = new_inode;
            }
        },
        Entry::File { name, next } => panic!("{}", name),
    };
}

fn read(filename: &str) -> HashMap<u32, Entry> {
    let lines: Vec<String> = std::fs::read_to_string(filename).unwrap().split("\n").map(|s| s.trim().to_string()).collect();

    let mut fs: HashMap<u32, Entry> = HashMap::new();

    let mut node: u32 = 0;
    fs.insert(node, Entry::Dir{ name: "".to_string(), next: None, target: None, last: None});

    for line in lines {
        let tokens: Vec<&str> = line.split(" ").collect();
        match tokens[0] {
            "$" => match tokens[1] {
                "cd" => {},
                "ls" => {},
                _ => panic!("{line}")
            },
            "dir" => {},
            _ => {}
        }
    }

    fs
}
