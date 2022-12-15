use std::slice::Iter;
use std::cmp::Ordering;

#[derive(Debug, Clone, PartialEq)]
enum Item {
    Scalar(i32),
    List(Vec<Item>),
}

#[derive(Debug)]
enum Token {
    Digit(char),
    Number(i32),
    BraceOpen,
    BraceClose,
    Comma,
}

fn main() {
    let filename = std::env::args().skip(1).next().unwrap();
    let lines = read(&filename);
    println!("{lines:?}");

    let mut items: Vec<Item> = lines.iter().map(|line| parse_line(line)).collect();
    let sep1: Item = parse_line(&String::from("[[2]]"));
    let sep2: Item = parse_line(&String::from("[[6]]"));
    items.push(sep1.clone());
    items.push(sep2.clone());

    println!("{items:?}");

    items.sort_by(|a, b| compare(a, b));
    for item in &items {
        println!("{item:?}");
    }

    let i1 = items.iter().position(|x| x == &sep1).unwrap() + 1;
    let i2 = items.iter().position(|x| x == &sep2).unwrap() + 1;
    let prod = i1 * i2;
    println!("{i1}, {i2}, {prod}");
}

fn compare(left: &Item, right: &Item) -> Ordering {
    match (left, right) {
        (Item::Scalar(s), Item::List(l)) => {
            compare(&Item::List(vec![Item::Scalar(*s)]), right)
        }
        (Item::List(l), Item::Scalar(s)) => {
            compare(left, &Item::List(vec![Item::Scalar(*s)]))
        }
        (Item::Scalar(l), Item::Scalar(r)) => {
            if l == r {
                Ordering::Equal
            } else if l < r {
                Ordering::Less
            } else {
                Ordering::Greater
            }
        }
        (Item::List(l), Item::List(r)) => {
            let mut c: Ordering = Ordering::Equal;
            for i in 0 .. std::cmp::min(l.len(), r.len()) {
                c = compare(&l[i], &r[i]);
                if c != Ordering::Equal {
                    break;
                }
            }
            if c == Ordering::Equal {
                if l.len() == r.len() {
                    Ordering::Equal
                } else if l.len() < r.len() {
                    Ordering::Less
                } else {
                    Ordering::Greater
                }
            } else {
                c
            }
        }
        (_, _) => {
            panic!("unknown types")
        }
    }
}

fn read(filename: &str) -> Vec<String> {
    std::fs::read_to_string(filename).unwrap().trim()
        .split("\n")
        .filter_map(|line| {
            match line.trim().len() {
                0 => None,
                _ => Some(line),
            }
        })
        .map(|line| line.to_string())
        .collect()
}

fn parse_list(token_iter: &mut Iter<Token>) -> Vec<Item> {
    let mut list: Vec<Item> = vec![];

    loop {
        let token = token_iter.next().unwrap();
        match token {
            Token::Number(v) => {
                list.push(Item::Scalar(*v));
            }
            Token::BraceOpen => {
                let item = Item::List(parse_list(token_iter));
                list.push(item);
            }
            Token::BraceClose => {
                break;
            }
            _ => {
            }
        }
    }
    list
}

fn parse_line(line: &String) -> Item {
    let tokens = lex(line).unwrap();

    let mut tokens_iter = tokens.iter();

    let first = tokens_iter.next().unwrap();
    let items = parse_list(&mut tokens_iter);
    Item::List(items)
}

fn lex(input: &String) -> Option<Vec<Token>> {
    let mut tokens: Vec<Token> = Vec::new();

    let mut it = input.chars().peekable();
    while let Some(&c) = it.peek() {
        match c {
            '0' ..= '9' | '-' => {
                it.next();
                tokens.push(Token::Digit(c));
            }
            '[' => {
                it.next();
                tokens.push(Token::BraceOpen);
            }
            ']' => {
                it.next();
                tokens.push(Token::BraceClose);
            }
            ',' => {
                it.next();
                tokens.push(Token::Comma);
            }
            ' ' => {
                it.next();
            }
            _ => {
                it.next();
            }
        }
    }

    let mut tokens2: Vec<Token> = Vec::new();
    let mut digits = String::new();
    for token in tokens {
        match token {
            Token::Digit(c) => {
                digits.push(c);
            }
            t => {
                if digits.len() > 0 {
                    let d = digits.parse::<i32>().unwrap();
                    tokens2.push(Token::Number(d));
                    digits.clear();
                }
                tokens2.push(t);
            }
        }
    }

    Some(tokens2)
}
