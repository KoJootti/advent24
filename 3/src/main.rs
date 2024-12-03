use std::usize::MAX;

const TEST_INPUT: &str = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))";

const INPUT_FILE: &str = "input.txt";
const MUL_KEYWORD: &str = "mul";
const DISABLE_CALL: &str = "don't()";
const ENABLE_CALL: &str = "do()";
const MUL_KW_COUNT: usize = 3;

#[derive(Debug)]
struct MulInput {
    x: i32,
    y: i32,
}

fn cut_to_index(input: &str, idx: usize) -> &str {
    let (_, right) = input.split_at(idx);
    return right;
}

fn parse_vals(input: &str) -> Option<MulInput> {
    let splitted = input.split_once(',');
    match splitted {
        Some((first, second)) => {
            let parsed1 = first.parse::<i32>();
            let parsed2 = second.parse::<i32>();
            if parsed1.is_err() || parsed2.is_err() {
                return None;
            }
            let (v1, v2) = (parsed1.unwrap_or(0), parsed2.unwrap_or(0));
            return Some(MulInput { x: v1, y: v2 });
        }
        None => {
            return None;
        }
    }
}

fn find_mul_vals_start(input: &str) -> (Option<MulInput>, usize) {
    let (_, mul_start) = input.split_at(MUL_KW_COUNT);
    if mul_start.chars().next() != Some('(') {
        return (None, 3);
    }
    let (_, mul_start) = mul_start.split_at(1);
    let end_idx = mul_start.find(')');
    match end_idx {
        Some(idx) => {
            let (vals, _) = mul_start.split_at(idx);
            let ret = parse_vals(vals);
            match ret {
                Some(mul_input) => {
                    return (Some(mul_input), 3);
                }
                None => {
                    return (None, 3);
                }
            }
        }
        None => {
            return (None, 3);
        }
    }
}

fn parse_input(mut input: &str) -> Vec<MulInput> {
    let mut result: Vec<MulInput> = Vec::new();
    let mut enabled = true;

    loop {
        let mul_chr_idx = input.find(MUL_KEYWORD).unwrap_or(MAX);
        let disable_call_idx = input.find(DISABLE_CALL).unwrap_or(MAX);
        let enable_call_idx = input.find(ENABLE_CALL).unwrap_or(MAX);

        if mul_chr_idx == MAX {
            break;
        }

        if !enabled {
            // If disabled and enable call not found, then we are done
            if enable_call_idx == MAX {
                break;
            }

            input = cut_to_index(input, enable_call_idx + ENABLE_CALL.len());
            enabled = true;
            continue;
        }

        if disable_call_idx < mul_chr_idx && disable_call_idx < enable_call_idx {
            enabled = false;
            input = cut_to_index(input, disable_call_idx + DISABLE_CALL.len());
            continue;
        }

        input = cut_to_index(input, mul_chr_idx);
        let (mul_input, idx) = find_mul_vals_start(input);
        match mul_input {
            Some(mul) => {
                result.push(mul);
                input = cut_to_index(input, idx);
            }
            None => {
                input = cut_to_index(input, idx);
            }
        }
    }

    return result;
}

fn calc_sum_of_mul(input: &Vec<MulInput>) -> i32 {
    let mut sum = 0;
    for mul in input {
        sum += mul.x * mul.y;
    }
    return sum;
}

fn read_input_file(file_name: &str) -> String {
    use std::fs::File;
    use std::io::Read;

    let mut file = File::open(file_name).expect("file not found");
    let mut contents = String::new();
    file.read_to_string(&mut contents)
        .expect("something went wrong reading the file");
    return contents;
}

fn main() {
    println!("With test data: ");
    let mul_vec = parse_input(TEST_INPUT);
    let res = calc_sum_of_mul(&mul_vec);
    println!("result: {:?}", res);

    println!("\nWith actual input: ");

    let input = read_input_file(INPUT_FILE);
    let mul_vec = parse_input(input.as_str());
    let res = calc_sum_of_mul(&mul_vec);
    println!("result: {:?}", res);
}
