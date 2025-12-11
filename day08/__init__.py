from dataclasses import dataclass
from functools import reduce
from pprint import pprint
from typing import Any, Callable, NamedTuple

from util import context

PUZZLE_1_EXPECTS = 40
PUZZLE_2_EXPECTS = 25272

class Point(NamedTuple):
  x: int
  y: int
  z: int

@dataclass
class PointPair():
  p1: Point
  p2: Point

type Circuit = set[str]

  # def __hash__(self) -> int:
  #   lesser = self.p1
  #   greater = self.p2
  #   if self.p2.x < self.p1.x or (
  #     self.p2.x == self.p1.x and self.p2.y < self.p1.y
  #   ) or (
  #     self.p2.x == self.p1.x and self.p2.y == self.p1.y and self.p2.z < self.p1.z
  #   ):
  #     lesser = self.p2
  #     greater = self.p1
  #   return f"{lesser}_{greater}"

@dataclass
class Ref[T]:
  item: T

  def __hash__(self) -> int:
    return id(self.item)
  

def parse_points(input: list[str]) -> list[Point]:
  return list(set((Point(*(int(c) for c in line.split(","))) for line in input)))

# as an optimization we dont care about taking 3rd root 
def calc_magnitude(p1: Point, p2: Point):
  return abs(reduce(
    lambda a, b: a + b,
    [ (p2[i]-p1[i]) ** 2 for i in range(len(p1))]
  ))

def join_key(p1: Point, p2: Point) -> str:
  return ",".join(str(c) for c in p1) + "-" + ",".join(str(c) for c in p2)

def get_pairs_by_shortest(points: list[Point])-> list[str]:
  all_dists = dict[str, int]()
  for i in range(len(points)):
    for j in range(len(points)):
      if i == j:
        continue

      p1 = points[i]
      p2 = points[j]

      if join_key(p2, p1) in all_dists: # avoid dupes
        continue

      all_dists[join_key(p1, p2)] = calc_magnitude(p1,p2)

  return sorted(
    all_dists,
    key= lambda k: all_dists[k]
  )

def pop_by_index[T](list: list[T], condition: Callable[[T], bool]):
  for i, el in enumerate(list):
    if condition(el):
      return list.pop(i)
  raise ValueError()

def prepare_circuits(point_pairs: list[str]) -> list[Circuit]:
  points = set[str]()
  for k in point_pairs:
    for p in k.split("-"):
      points.add(p)

  return [{p} for p in points]


def solve_puzzle_1(input: list[str]) -> Any:
  points = parse_points(input)

  pairs_by_shortest = get_pairs_by_shortest(points)

  amount = 10 if context.is_test else 1000
  circuits: list[Circuit] = []
  
  circuits = prepare_circuits(pairs_by_shortest[:amount])

  for k in pairs_by_shortest[:amount]:
    p1, p2 = k.split("-")

    circuit1 = pop_by_index(circuits, lambda c: p1 in c)

    if p2 in circuit1:
      circuits.append(circuit1)
      continue

    circuit2 = pop_by_index(circuits, lambda c: p2 in c)

    circuits.append(circuit1.union(circuit2))

  largest_circuits = sorted(circuits, key=lambda c: len(c), reverse=True)[:3]

  return reduce(
    lambda a, b: a * b,
    (len(c) for c in largest_circuits)
  )

def solve_puzzle_2(input: list[str]) -> Any:
  points = parse_points(input)

  pairs_by_shortest = get_pairs_by_shortest(points)

  circuits: list[Circuit] = []
  
  circuits = prepare_circuits(pairs_by_shortest)

  last_connection: tuple[str, str]
  
  for k in pairs_by_shortest:
    p1, p2 = k.split("-")

    circuit1 = pop_by_index(circuits, lambda c: p1 in c)

    if p2 in circuit1:
      circuits.append(circuit1)
      continue

    circuit2 = pop_by_index(circuits, lambda c: p2 in c)

    # A union is considered a connection 
    circuits.append(circuit1.union(circuit2))
    last_connection = (p1, p2)

  if len(circuits) != 1:
    raise Exception(f"len of of circuits is not 1 (is {len(circuits)})")

  return reduce(
    lambda a, b: a * b,
    [int(c.split(",")[0]) for c in last_connection]
  )
