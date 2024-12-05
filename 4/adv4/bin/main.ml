let test_input = "MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX" ;;
let search_term = "XMAS" ;;
(* Traditional directions of wind *)
type direction = N | E | S | W | NE | SE | SW | NW ;;

let input_to_2d_array input =
  let lines = String.split_on_char '\n' input in
  let array = Array.make_matrix (List.length lines) (String.length (List.hd lines)) ' ' in
  List.iteri (fun i line ->
    String.iteri (fun j c ->
      array.(i).(j) <- c
    ) line
  ) lines;
  array ;;

input_to_2d_array test_input ;;

