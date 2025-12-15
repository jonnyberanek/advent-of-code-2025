
from functools import reduce
from typing import overload


def multiply(*args: int) -> int:
  return reduce(
    lambda a, b: a * b,
    args 
  )