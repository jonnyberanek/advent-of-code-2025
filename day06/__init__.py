from dataclasses import dataclass
from pprint import pprint
from typing import Any, Callable
from re import compile
from functools import reduce

PUZZLE_1_EXPECTS = 4277556
PUZZLE_2_EXPECTS = 3263827

@dataclass
class MathProblem():
  operands: list[int]
  operation: Callable[[int, int], int]

def add(a:int, b:int):
  return a + b

def mult(a:int, b:int):
  return a * b

def parse_operator(operator: str):
  return add if operator == "+" else mult

def calculate_grand_total(problems: list[MathProblem]):
  return sum(
    reduce(
      problem.operation,
      problem.operands,
      0 if problem.operation is add else 1
    ) for problem in problems
  )

def solve_puzzle_1(input: list[str]) -> Any:
  reg = compile(r' +')

  split_input = [reg.split(line.lstrip()) for line in input]

  problems: list[MathProblem] = []

  for i in range(0, len(split_input[0])):
    operands = []
    for j in range(0, len(input) - 1): # all but last line (operator)
      operands.append(int(split_input[j][i]))
    
    operation = parse_operator(split_input[len(input)-1][i])
    
    problems.append(MathProblem(operands, operation))
  
  return calculate_grand_total(problems)

def solve_puzzle_2(input: list[str]) -> Any:
  problems: list[MathProblem] = []

  operator_reg = compile(r'[\+\*]')

  operators = input[len(input) - 1]
  iter_op = operator_reg.finditer(operators)
  op_curr = next(iter_op)
  while op_curr: 
    # maybe this part could be shortened with lookahead
    op_next = next(iter_op, None)
    end: int #exclusive
    if not op_next:
      end = max(len(line) for line in input)  ## is a fix for rstripping input
    else:
      end = op_next.start(0) - 1
    

    operands = []
    for i in range(op_curr.start(0), end):
      num_str = ""
      for line in input[:len(input) - 1]:
        if i >= len(line) or line[i] == " ":
          continue
        num_str += line[i]
      operands.append(int(num_str))

    problems.append(
      MathProblem(
      operands,
      parse_operator(op_curr.group(0))
      )
    )

    op_curr = op_next
  
  return calculate_grand_total(problems)
