from typing import Any

PUZZLE_1_EXPECTS = 3
PUZZLE_2_EXPECTS = 6

def solve_puzzle_1(input: list[str]) -> Any:
  pos = 50
  count_zero = 0
  for instr in input:
    change = int(instr[1:])
    if instr[0] == "L":
      change *= -1

    pos = (pos + change) % 100
    
    if pos == 0:
      count_zero += 1

  return count_zero

def solve_puzzle_2(input: list[str]) -> Any:
  pos = 50
  count_zero = 0
  for instr in input:
    change = int(instr[1:])
    if instr[0] == "L":
      change *= -1

    excess_turns = int(change / 100)
    change -= excess_turns * 100

    count_zero += abs(excess_turns)

    initial = pos
    pos = pos + change

    # There may be a better way to avoid counting moves from 0?
    if (initial != 0 and pos <= 0) or pos >= 100:
      count_zero += 1
    
    pos %= 100

  return count_zero
