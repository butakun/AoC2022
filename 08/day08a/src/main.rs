use ndarray::{Array1, Array2, ArrayView1};

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let filename = &args[1];

    let G = read(filename);
    println!("{G}");

    let mut Vl: Array2<i32> = Array2::zeros(G.raw_dim());
    let mut Vr: Array2<i32> = Array2::zeros(G.raw_dim());;
    for i in 0..(G.shape()[0]) {
        let vl;
        let vr;
        (vl, vr) = visible(G.row(i));
        Vl.row_mut(i).assign(&vl);
        Vr.row_mut(i).assign(&vr);
    }

    let mut Vu: Array2<i32> = Array2::zeros(G.raw_dim());
    let mut Vd: Array2<i32> = Array2::zeros(G.raw_dim());;
    for j in 0..(G.shape()[1]) {
        let vu;
        let vd;
        (vu, vd) = visible(G.column(j));
        Vu.column_mut(j).assign(&vu);
        Vd.column_mut(j).assign(&vd);
    }
    let V = &Vl | &Vr | &Vu | &Vd;
    println!("V");
    println!("{V}, {}", V.sum());
}

fn visible(g: ArrayView1<i32>) -> (Array1<i32>, Array1<i32>) {
    let idim = g.shape()[0];
    let mut vl: Array1<i32> = Array1::zeros(g.raw_dim());
    let mut vr: Array1<i32> = Array1::zeros(g.raw_dim());

    for i in 0..idim {
        let mut hmax = -1;
        for ii in 0..i {
            if g[ii] > hmax {
                hmax = g[ii];
                vl[ii] = 1;
            }
        }
    }

    for i in (0..idim).rev() {
        let mut hmax = -1;
        for ii in ((i+1)..idim).rev() {
            if g[ii] > hmax {
                hmax = g[ii];
                vr[ii] = 1;
            }
        }
    }
    (vl, vr)

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
