from typing import Any

PUZZLE_1_EXPECTS = 13
PUZZLE_2_EXPECTS = 43

"""
-1, -1 | -1, 0 | -1, 1
 0, -1 |  0, 0 |  0, 1
 1, -1 |  1, 0 |  1, 1
"""
def get_all_neighbors(grid: list[list[bool]], x: int, y: int) -> list[bool]:
  neighbors = []
  if x > 0:
    neighbors.append(grid[y][x-1])
    if y > 0:
      neighbors.append(grid[y-1][x-1])
    if y < len(grid)-1:
      neighbors.append(grid[y+1][x-1])
  
  if x < len(grid[y])-1:
    neighbors.append(grid[y][x+1])
    if y > 0:
      neighbors.append(grid[y-1][x+1])
    if y < len(grid)-1:
      neighbors.append(grid[y+1][x+1])

  if y > 0:
    neighbors.append(grid[y-1][x])

  if y < len(grid)-1:
    neighbors.append(grid[y+1][x])
  
  return neighbors

def count_true(l: list[bool]):
  return len([e for e in l if e])


def solve_puzzle_1(input: list[str]) -> Any:
  # grid[y][x]
  grid = [[char == "@" for char in line.rstrip()] for line in input]

  is_accessible_grid = [[count_true(get_all_neighbors(grid, x, y)) < 4 for x, is_roll in enumerate(line) if is_roll] for y, line in enumerate(grid)]

  return len(
    [item for sublist in is_accessible_grid for item in sublist if item]
  )

def solve_puzzle_2(input: list[str]) -> Any:
  # grid[y][x]
  grid = [[char == "@" for char in line.rstrip()] for line in input]

  count = 0
  last_count = -1
  while count > last_count:
    last_count = count
    for y, line in enumerate(grid):
      for x, is_roll in enumerate(line):
        if not is_roll:
          continue

        if count_true(get_all_neighbors(grid, x, y)) < 4:
          grid[y][x] = False # aka take roll
          count += 1

  return count
