from dataclasses import dataclass, field
from pprint import pprint
from typing import Any, Self, Sequence

PUZZLE_1_EXPECTS = 5
PUZZLE_2_EXPECTS = 2

@dataclass
class Device:
  id: str
  ouputs: list[str] = field(default_factory=list)

def parse_devices(input: list[str]) -> dict[str, Device]:
  outputs_by_id = dict()
  for line in input:
    id, rest = line.split(": ")
    outputs_by_id[id] = Device(id, rest.split(" "))
  
  return outputs_by_id

def solve_puzzle_1(input: list[str]) -> Any:
  devices = parse_devices(input)
  
  def find_path_count_brute_force(curr: Device, devices: dict[str, Device], visited_count: int = 0)-> int:
    
    if visited_count > len(devices):
      raise Exception("There are loops")

    return sum(
      1 if id == 'out' else find_path_count_brute_force(devices[id], devices, visited_count + 1)
      for id in curr.ouputs
    )

  return find_path_count_brute_force(devices['you'], devices)

fft = 0b01
dac = 0b10
all_flags = fft ^ dac

## aka for each flag state, how many paths does this produce?
type Outcomes = dict[int, int]

def solve_puzzle_2(input: list[str]) -> Any:
  devices = parse_devices(input)
  
  ## Tracks a device's count of paths leading to "out" per state (see below)
  # A state is a set of flags which translate to which target devices (fft & dac) this segment visits 
  known_paths = dict[str, Outcomes]()
  def find_outcomes(curr: Device, devices: dict[str, Device], visited_count: int = 0) -> Outcomes:
    if visited_count > len(devices):
      raise Exception("There are loops")

    if curr.id in known_paths:
      return known_paths[curr.id]
      
    flag = 0
    if curr.id == 'fft':
      flag = fft
    elif curr.id == 'dac':
      flag = dac
      
    outcomes: Outcomes = {
      0: 0,
      fft: 0,
      dac: 0,
      all_flags: 0
    }
    for id in curr.ouputs:
      if id == 'out':
        outcomes[flag] += 1
      else:
        for k, v in find_outcomes(devices[id], devices, visited_count + 1).items():
          outcomes[k | flag] += v

    known_paths[curr.id] = outcomes
    
    return outcomes

  return find_outcomes(devices['svr'], devices)[all_flags]
