from typing import Any

PUZZLE_1_EXPECTS = 357
PUZZLE_2_EXPECTS = 3121910778619

def parse_input(input: list[str]) -> list[list[int]]:
  return [[int(jolt) for jolt in bank.rstrip()] for bank in input]

def solve_puzzle_1(input: list[str]) -> Any:
  banks = parse_input(input)
  
  total = 0
  for bank in banks:
    max_tens = 0
    max_tens_i = -1
    for i, jolt in enumerate(bank[:-1]): # last number can't be first digit
      if jolt > max_tens:
        max_tens_i = i
        max_tens = jolt

    max_ones = 0
    for i, jolt in enumerate(bank[max_tens_i+1:]):
      if jolt > max_ones:
        max_ones = jolt

    total += max_tens * 10 + max_ones
  
  return total
      

def solve_puzzle_2(input: list[str]) -> Any:
  banks = parse_input(input)
  
  total = 0
  # AKA each digit
  num_digits = 12
  for jolts in banks:
    maxes = [0] * num_digits
    last_max_idx = -1
    # Iterate through each digit
    for i, _ in enumerate(maxes):

      # Joltage must be positioned after last
      # Starting after last max's index, find max value
      for j in range(last_max_idx+1, len(jolts) - num_digits + i + 1):
        if jolts[j] > maxes[i]:
          maxes[i] = jolts[j]
          last_max_idx = j

    # Sum digits using powers of 10 according to index
    total += sum(x*10**(num_digits - i - 1) for i, x in enumerate(maxes))
  
  return total
