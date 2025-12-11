import importlib
from sys import argv
from argparse import ArgumentParser

from util import context

parser = ArgumentParser(
  prog="aoc",
  description="Advent of Code 2025 Runner"
)

parser.add_argument("day", type=int)
parser.add_argument("puzzle", type=int, choices=[1,2])
parser.add_argument("-t", "--test", action='store_true')


if __name__ == "__main__":
  args = parser.parse_args(argv[1:])
  day_dir = f"day{int(args.day):0>2}"

  module = importlib.import_module(day_dir)

  print(f"Running {day_dir} puzzle {args.puzzle}..")

  if args.test:
    context.is_test = True

  solution = None
  with open(f"{day_dir}/data_{"test" if args.test else "real"}.txt") as f:
    input = [line.rstrip() for line in f.readlines()]
    solution = getattr(module, f"solve_puzzle_{args.puzzle}")(input)

  if args.test:
    expected = getattr(module, f"PUZZLE_{args.puzzle}_EXPECTS")
    if solution != expected:
      print(f"Incorrect Solution: '{solution}' should be '{expected}'")
      exit(1)
    print("Test passed :)")

  else:
    print(f"Solution is: {solution}")