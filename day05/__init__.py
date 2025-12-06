from dataclasses import dataclass
from typing import Any, NamedTuple

PUZZLE_1_EXPECTS = 3
PUZZLE_2_EXPECTS = 14

"""Inclusive Bounds"""
class Bounds(NamedTuple):
  start: int
  end: int

  def __contains__(self, key: int) -> bool:
    return self.start <= key and self.end >= key

@dataclass
class Inventory:
  fresh_ranges: list[Bounds]
  ingredients: list[int]

def parse_inventory(input: list[str]):
  split_idx = input.index("")
  return Inventory(
    [Bounds(*(int(id) for id in line.split("-"))) for line in input[:split_idx]],
    [int(id) for id in input[split_idx+1:]]
  )


def solve_puzzle_1(input: list[str]) -> Any:
  inv = parse_inventory(input)

  return len(
    [id for id in inv.ingredients if any(id in r for r in inv.fresh_ranges)]
  )


def solve_puzzle_2(input: list[str]) -> Any:
  ranges = parse_inventory(input).fresh_ranges
  
  ranges.sort(key = lambda r: float(f"{r.start}.{r.end}")) # hacky, but.. eh

  # If ranges are sorted then we can assume each successive end bound is the
  #  "border" of existing ids
  id_count = 0
  highest_id_yet: int = -1
  for bounds in ranges:
    start = bounds.start
    if start <= highest_id_yet:
      if bounds.end <= highest_id_yet:
        continue
      start = highest_id_yet + 1

    id_count += bounds.end - start + 1

    highest_id_yet = bounds.end

  return id_count
