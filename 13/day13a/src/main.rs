use std::slice::Iter;

#[derive(Debug)]
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
    let pairs = read(&filename);
    println!("{pairs:?}");

    let mut sum = 0;
    for (i, pair) in pairs.into_iter().enumerate() {
        let left = parse_line(&pair.0);
        let right = parse_line(&pair.1);
        println!("parsed left: {left:?}");
        println!("parsed rifght: {right:?}");
        let c = compare(&left, &right);
        println!("compare = {c}");
        if c == 1 {
            println!("Pair {} is correct.", i+1);
            sum += i + 1;
        }
    }
    println!("sum = {sum}");
}

fn compare(left: &Item, right: &Item) -> i32 {
    match (left, right) {
        (Item::Scalar(s), Item::List(l)) => {
            compare(&Item::List(vec![Item::Scalar(*s)]), right)
        }
        (Item::List(l), Item::Scalar(s)) => {
            compare(left, &Item::List(vec![Item::Scalar(*s)]))
        }
        (Item::Scalar(l), Item::Scalar(r)) => {
            if l == r {
                0
            } else if l < r {
                1
            } else {
                -1
            }
        }
        (Item::List(l), Item::List(r)) => {
            let mut c: i32 = 0;
            for i in 0 .. std::cmp::min(l.len(), r.len()) {
                c = compare(&l[i], &r[i]);
                if c != 0 {
                    break;
                }
            }
            if c == 0 {
                if l.len() == r.len() {
                    0
                } else if l.len() < r.len() {
                    1
                } else {
                    -1
                }
            } else {
                c
            }
        }
        (_, _) => {
            0
        }
    }
}

fn read(filename: &str) -> Vec<(String, String)> {
    std::fs::read_to_string(filename).unwrap().trim()
        .split("\n\n")
        .map(|twolines| {
            let lines = twolines.split("\n")
                .collect::<Vec<&str>>();
            (lines[0].to_string(), lines[1].to_string())
        })
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
