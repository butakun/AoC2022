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

    for pair in pairs {
        let left = parse_list(&pair.0);
        let right = parse_list(&pair.1);
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

fn parse_list(line: &String) {
    let tokens = lex(line).unwrap();
    println!("{tokens:?}");

    let mut stack: Vec<Item> = Vec::new();

    let mut currentItem = Item::Scalar(0);
    for token in tokens {
        match &token {
            BraceOpen => {
                currentItem = Item::List(Vec::new());
            }
            BraceClose => {
                let mut parent = stack.pop().unwrap();
                if let Item::List(ref mut l) = parent {
                    l.push(currentItem);
                }
                stack.push(parent);
            }
            Token::Number(v) => {
                if let Item::List(ref mut l) = currentItem {
                    l.push(Item::Scalar(*v));
                }
            }
        }
    }
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
