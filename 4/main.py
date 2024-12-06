from enum import Enum
input_file = "input.txt"

search_term = "XMAS"

test_input = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""


class Direction(Enum):
  UP = "UP"
  DOWN = "DOWN"
  LEFT = "LEFT"
  RIGHT = "RIGHT"
  UP_LEFT = "UP_LEFT"
  UP_RIGHT = "UP_RIGHT"
  DOWN_LEFT = "DOWN_LEFT"
  DOWN_RIGHT = "DOWN_RIGHT"

direction_to_coord = {
  Direction.UP: (-1, 0),
  Direction.DOWN: (1, 0),
  Direction.LEFT: (0, -1),
  Direction.RIGHT: (0, 1),
  Direction.UP_LEFT: (-1, -1),
  Direction.UP_RIGHT: (-1, 1),
  Direction.DOWN_LEFT: (1, -1),
  Direction.DOWN_RIGHT: (1, 1),
}

def input_to_2d_array(input: str) -> list[list[str]]:
  return [list(line) for line in input.split("\n")]

def find_all_first_search_term_occurences(arr: list[list[str]]) -> list[tuple[int, int]]:
  occurences = []
  first_char = search_term[0]
  for i, row in enumerate(arr):
    for j, char in enumerate(row):
      if char == first_char:
        occurences.append((i, j))
  return occurences

def is_direction_valid(coord: tuple[int,int], direction: Direction, arr: list[list[str]]) -> bool:
  direction_coords = direction_to_coord[direction]
  y, x = coord
  new_y = y + (direction_coords[0] * (len(search_term) - 1))
  new_x = x + (direction_coords[1] * (len(search_term) - 1))
  if new_y < 0 or new_y >= len(arr):
    return False
  if new_x < 0 or new_x >= len(arr[new_y]):
    return False
  return True




def find_all_search_occurences_starting_from_position(coord: tuple[int, int], arr: list[list[str]]) -> set[Direction]:
  directions = set()
  # Check all directions
  for direction in Direction:
    if not is_direction_valid(coord=coord, direction=direction, arr=arr):
      continue

    seach_term_in_direction = False
    direction_coords = direction_to_coord[direction]
    for i in range(len(search_term)):
      new_i = coord[0] + direction_coords[0] * (i)
      new_j = coord[1] + direction_coords[1] * (i)
      char = arr[new_i][new_j]
      expected_char = search_term[i]
      if char != expected_char:
        break

      if i == (len(search_term) - 1):
        seach_term_in_direction = True

    if seach_term_in_direction:
      directions.add(direction)

  return directions

def solve(input: str) -> int:
  arr = input_to_2d_array(input=input)
  first_term_occurences = find_all_first_search_term_occurences(arr=arr)
  sum_of_occurences = 0
  for coord in first_term_occurences:
    directions = find_all_search_occurences_starting_from_position(coord=coord, arr=arr)
    sum_of_occurences += len(directions)

  return sum_of_occurences

def main():
  answer = solve(test_input)
  print("Answer:", answer)
  with open(input_file, "r") as file:
    file_input = file.read()
    answer = solve(file_input)
    print("Real answer:", answer)


if __name__ == '__main__':
  main()
