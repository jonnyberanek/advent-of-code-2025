from functools import reduce

def multiply(*args: int) -> int:
  return reduce(
    lambda a, b: a * b,
    args 
  )