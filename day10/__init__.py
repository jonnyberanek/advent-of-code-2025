from dataclasses import dataclass, field
from functools import reduce
from pprint import pprint
from typing import Any
import re

from util.logger import logger

PUZZLE_1_EXPECTS = 7
PUZZLE_2_EXPECTS = 33

type ButtonWirings = set[int]
type Joltages = tuple[int, ...]

@dataclass
class Machine:
  expected_light_states: int
  button_actions: list[ButtonWirings]
  joltages_requirements: Joltages

  def actions_to_bits(self):
    for action in self.button_actions:
      yield reduce(
        lambda acc, cur: acc + (1 << cur),
        [int(n) for n in action],
        0
      )


def parse_machines(input: list[str]) -> list[Machine]:

  regex_lights = re.compile(r'\[(.+)\]')
  regex_wirings = re.compile(r'\((.+?)\)')
  regex_joltages = re.compile(r'\{(.+)\}')

  def state_to_bits(text: str) -> int:
    return int("".join(reversed(text.replace("#", "1").replace(".", "0"))), 2)
  
  return [Machine(
    expected_light_states=state_to_bits(regex_lights.search(line).group(1)), # pyright: ignore[reportOptionalMemberAccess]
    button_actions=[{int(i) for i in m.split(",")} for m in regex_wirings.findall(line)], 
    joltages_requirements=tuple(int(i) for i in regex_joltages.search(line).group(1).split(",")) # pyright: ignore[reportOptionalMemberAccess]
  ) for line in input]

@dataclass
class PossibleSolution:
  state: int = 0b0
  steps: list[int] = field(default_factory=list)
  
  def __str__(self) -> str:
    return f"Solution: {self.state:06b} ({", ".join(f"{s:06b}" for s in self.steps)})"

def solve_puzzle_1(input: list[str]) -> Any:
  machines = parse_machines(input)

  def find_least_presses_brute_force(machine: Machine):
    sols: set[int] = {0b0}
    iters = 0
    while True:
      iters += 1
      if iters > 1000:
        raise Exception("Something is wrong...")

      new_sols = set[int]()
      for action in machine.actions_to_bits():
        for sol in sols:
          new_sol = sol ^ action
          if new_sol == 0b0:
            # ignore
            continue

          if new_sol == machine.expected_light_states:
            logger.t(f"found in {iters} steps")
            return iters
          new_sols.add(new_sol)
      sols = new_sols

  return sum(find_least_presses_brute_force(m) for m in machines)        


def solve_puzzle_2(input: list[str]) -> Any:
  machines = parse_machines(input)

  # Works for test data, hangs for real
  def find_least_presses_brute_force(machine: Machine):
    states: set[Joltages] = {tuple([0] * len(machine.joltages_requirements))}
    iters = 0
    while True:
      iters += 1
      if iters > 1000:
        raise Exception("Something is wrong...")

      new_states = set[Joltages]()
      for state in states:
        for actions in machine.button_actions:
          new_state = tuple([ jolt + 1 if (i in actions) else jolt for i, jolt in enumerate(state)])

          if new_state == machine.joltages_requirements:
            logger.t(f"found in {iters} steps")
            return iters
          
          if (
            # Exceeded requirements
            any(state[i] > jolt_r for i, jolt_r in enumerate(machine.joltages_requirements))
          ):
            # aka discard
            continue

          new_states.add(new_state)
      states = new_states
  
  # Works for test data, hangs for real
  def find_least_presses_2(machine: Machine):

    def find_min(state, actions):
      pass


    states: set[Joltages] = {tuple([0] * len(machine.joltages_requirements))}
    iters = 0
    while True:
      iters += 1
      if iters > 1000:
        raise Exception("Something is wrong...")

      new_states = set[Joltages]()
      for state in states:
        for actions in machine.button_actions:
          new_state = tuple([ jolt + 1 if (i in actions) else jolt for i, jolt in enumerate(state)])

          if new_state == machine.joltages_requirements:
            logger.t(f"found in {iters} steps")
            return iters
          
          if (
            # Exceeded requirements
            any(state[i] > jolt_r for i, jolt_r in enumerate(machine.joltages_requirements))
          ):
            # aka discard
            continue

          new_states.add(new_state)
      states = new_states

  return sum(find_least_presses_brute_force(m) for m in machines)        
