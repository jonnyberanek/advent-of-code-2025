from typing import Any, NamedTuple

PUZZLE_1_EXPECTS = 1227775554
PUZZLE_2_EXPECTS = 4174379265

class Bounds(NamedTuple):
  start: int
  end: int

def get_ids(input: list[str]) -> list[int]:
  bounds_list = [Bounds(*(int(b) for b in r.split("-",1))) for r in input[0].strip().split(",")]
  ids = [range(b.start, b.end+1) for b in bounds_list]
  return [b for r in ids for b in r]

def solve_puzzle_1(input: list[str]) -> Any:
  ids = get_ids(input)

  def is_unique(id: int):
    id_str = str(id)
    num_digits = len(id_str)
    
    if num_digits % 2 == 1: # odd can't only be repeated
      return True
    
    split = num_digits // 2
    return id_str[:split] != id_str[split:]

  return sum(id for id in ids if not is_unique(id))

def solve_puzzle_2(input: list[str]) -> Any:
  ids = get_ids(input)

  def is_repeated(id: int):
    id_str = str(id)
    num_digits = len(id_str)
    
    for i in range(0, num_digits // 2 + 2):
      interval_length = i + 1
      if num_digits // interval_length < 2 or num_digits % interval_length != 0:
        #aka cannot evenly repeat in this interval
        continue
      
      first = id_str[:interval_length]
      is_repeated = True
      for j in range(1, num_digits // interval_length):
        start = j*interval_length
        if first != id_str[start:start+interval_length]:
          is_repeated = False
          break

      if is_repeated:
        return True
      
    return False

  return sum(id for id in ids if is_repeated(id))
