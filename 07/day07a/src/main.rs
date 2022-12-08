use std::collections::HashMap;

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let filename = &args[1];
    let fs = read(filename);

    println!("{:?}", fs);
}

fn read(filename: &str) -> HashMap<String, u32> {
    let lines: Vec<String> = std::fs::read_to_string(filename).unwrap().trim().split("\n").map(|s| s.trim().to_string()).collect();

    let mut fs: HashMap<String, u32> = HashMap::new();
    let mut node: Vec<String> = Vec::new();
    let mut size_this_dir: u32 = 0;

    for line in lines {
        let tokens: Vec<&str> = line.trim().split(" ").collect();
        println!("{:?}", tokens);
        match tokens[0] {
            "$" => match tokens[1] {
                "cd" => {
                    match tokens[2] {
                        ".." => {
                            let this_node = node.join("/");
                            let this_node_size = fs.get(&this_node).unwrap();
                            node.pop();
                            fs.entry(node.join("/")).and_modify(|e| *e += this_node_size);
                        },
                        _ => { node.push(tokens[2].to_string()); }
                    };
                },
                _ => {},
            },
            "dir" => {
                let new_node = format!("{}/{}", node.join("/"), tokens[1]);
                fs.insert(new_node, 0);
            },
            file => {
                let new_node = format!("{}/{}", node.join("/"), tokens[1]);
                let size: u32 = tokens[0].parse().unwrap();
                size_this_dir += size;
                println!("inserting {new_node}, size {size}");
                fs.insert(new_node, size);
                fs.entry(node.join("/")).and_modify(|e| *e += size);
            }
        };
    }

    fs
}
