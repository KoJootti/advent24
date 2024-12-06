import functools

test_input = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

OBSTACLE_CHAR = "#"
GUARD_CHARS = ("^", "v", "<", ">")
USED_CHAR = "X"

def is_position_in_grid(grid: list[list[str]], position: tuple[int,int]) -> bool:
  x, y = position
  return 0 <= x < len(grid[0]) and 0 <= y < len(grid)

def is_position_obstacle(grid: list[list[str]], position: tuple[int,int]) -> bool:
  x, y = position
  return grid[y][x] == OBSTACLE_CHAR

def get_guard_position_and_next_position(grid: list[list[str]]) -> tuple[tuple[int,int], tuple[int,int]]:
  for y, row in enumerate(grid):
    for x, cell in enumerate(row):
      if cell in GUARD_CHARS:
        if cell == "^":
          next_pos = (x, y - 1)
        elif cell == "v":
          next_pos = (x, y + 1)
        elif cell == "<":
          next_pos = (x - 1, y)
        elif cell == ">":
          next_pos = (x + 1, y)

        return (x, y), next_pos

  print("Guard not found")
  return None, None

def turn_right(direction: str) -> str:
  if direction not in GUARD_CHARS:
    raise ValueError(f"{direction} is not a valid guard direction")

  if direction == "^":
    return ">"
  elif direction == ">":
    return "v"
  elif direction == "v":
    return "<"
  elif direction == "<":
    return "^"

def advance_guard(grid: list[list[str]]) -> list[list[str]]:
  (guard_position, next_position) = get_guard_position_and_next_position(grid)
  if not guard_position or not next_position:
    return grid

  if is_position_in_grid(grid, next_position):
    if is_position_obstacle(grid, next_position):
      # Turn right
      grid[guard_position[1]][guard_position[0]] = turn_right(grid[guard_position[1]][guard_position[0]])
    else:
      # Move
      grid[next_position[1]][next_position[0]] = grid[guard_position[1]][guard_position[0]]
      # Clear the previous position and mark it as used
      grid[guard_position[1]][guard_position[0]] = USED_CHAR


    return grid

  # Clear the previous position and mark it as used if the guard is moving out of bounds
  grid[guard_position[1]][guard_position[0]] = USED_CHAR
  return grid

def solve(input: str) -> int:
  grid = [list(line) for line in input.split("\n") if line]

  while True:
    grid = advance_guard(grid)
    if not get_guard_position_and_next_position(grid)[0]:
      break

  for row in grid:
    print(row)

  used_positions = functools.reduce(lambda acc, row: acc + row.count(USED_CHAR), grid, 0)

  return used_positions

def main():
  test_answer = solve(test_input)

  with open("input.txt") as f:
    actual_input = f.read().strip()

  answer = solve(actual_input)
  print(f"Test answer: {test_answer}")
  print(f"Answer: {answer}")

if __name__=='__main__':
  main()
