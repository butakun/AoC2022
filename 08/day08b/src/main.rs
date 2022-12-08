use ndarray::{Array1, Array2, ArrayView1};
use ndarray_stats::QuantileExt;

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let filename = &args[1];

    let G = read(filename);
    println!("{G}");

    let mut Vr: Array2<i32> = Array2::zeros(G.raw_dim());
    let mut Vl: Array2<i32> = Array2::zeros(G.raw_dim());
    for i in 0..(G.shape()[0]) {
        let vr;
        let vl;
        (vr, vl) = view(G.row(i));
        Vr.row_mut(i).assign(&vr);
        Vl.row_mut(i).assign(&vl);
    }

    println!("Vr");
    println!("{Vr}");
    println!("Vl");
    println!("{Vl}");

    let mut Vd: Array2<i32> = Array2::zeros(G.raw_dim());
    let mut Vu: Array2<i32> = Array2::zeros(G.raw_dim());
    for j in 0..(G.shape()[1]) {
        let vd;
        let vu;
        (vd, vu) = view(G.column(j));
        Vd.column_mut(j).assign(&vd);
        Vu.column_mut(j).assign(&vu);
    }
    println!("Vd");
    println!("{Vd}");
    println!("Vu");
    println!("{Vu}");

    let V = &Vl * &Vr * &Vd * &Vu;
    println!("V");
    println!("{V}, {}", V.max().unwrap());
}

fn view(g: ArrayView1<i32>) -> (Array1<i32>, Array1<i32>) {
    let idim = g.shape()[0];
    let mut vr: Array1<i32> = Array1::zeros(g.raw_dim());
    let mut vl: Array1<i32> = Array1::zeros(g.raw_dim());

    for i in 0..idim {
        let mut cansee = 0;
        for ii in i+1..idim {
            cansee += 1;
            if g[ii] >= g[i] {
                break;
            }
        }
        vr[i] = cansee;
    }

    for i in 1..idim {
        let mut cansee = 0;
        for ii in (0..i).rev() {
            cansee += 1;
            if g[ii] >= g[i] {
                break;
            }
        }
        vl[i] = cansee;
    }
    (vr, vl)

}

fn read(filename: &str) -> Array2<i32> {
    let lines: Vec<String> = std::fs::read_to_string(filename).unwrap().trim().split("\n").map(|l| l.to_string()).collect();

    let idim = lines.len();
    let jdim = lines.iter().next().unwrap().len();
    println!("jdim = {jdim}");

    let mut G: Array2<i32> = Array2::zeros((idim, jdim));
    for (i, line) in lines.iter().enumerate() {
        let d: Vec<i32> = line.chars().map(|c| c.to_digit(10).unwrap().try_into().unwrap()).collect();
        for j in 0..jdim {
            G.row_mut(i)[j] = d[j];
        }
    }
    G
}
