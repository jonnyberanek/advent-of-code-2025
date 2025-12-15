from typing import NamedTuple, Self
from unittest import TestCase

class Point(NamedTuple):
  x: int
  y: int

def is_between(target: int, bound1: int, bound2: int) -> bool:
  return target > min(bound1, bound2) and target < max(bound1, bound2)

class Edge(tuple[Point, Point]):
  """An edge made by two points; assumed to be either horizontal or vertical"""
  
  # Kind of intersects, doesn't count if on same line (i.e. a.x = 5 and b.x = 5)
  def crosses(self, other: Self) -> bool:
    is_vertical = self[0].x == self[1].x
    if not is_vertical:
      if self[0].y != self[1].y:
        raise Exception("Something is wrong - Should not be diagonal")

    # colinear case - aka both horionztal or vertical
    if (
      (is_vertical and other[0].x == other[1].x) or
      (not is_vertical and other[0].y == other[1].y)
    ):
      if is_vertical and other[0].x == self[0].x:
        if is_between(other[0].y, self[0].y, self[1].y) or is_between(other[1].y, self[0].y, self[1].y):
        # Aka self line must go beyond one of other's points
          return True

      elif not is_vertical and other[0].y == self[0].y:
        if is_between(other[0].x, self[0].x, self[1].x) or is_between(other[1].x, self[0].x, self[1].x):
          return True

      return False
    
    if is_vertical:
      return is_between(self[0].x, other[0].x, other[1].x) and is_between(other[0].y, self[0].y, self[1].y)
    else:
      return is_between(self[0].y, other[0].y, other[1].y) and is_between(other[0].x, self[0].x, self[1].x)

class Polygon(list[Point]):
  def get_edges(self):
    for i in range(len(self)-1):
      yield Edge((self[i], self[i+1]))
    # optimizes last edge case
    yield Edge((self[len(self)-1], self[0]))


class edge_crosses(TestCase):

  def test_returns_false_when_parallel(self):
    self.assertFalse(
      Edge((Point(0,0), Point(0,5))).crosses(Edge((Point(2,0), Point(2,5))))
    )

  def test_returns_false_when_same_line(self):
    self.assertFalse(
      Edge((Point(0,0), Point(0,5))).crosses(Edge((Point(0,0), Point(0,5))))
    )

  def test_returns_true_when_colinear_and_partially_contained(self):
    self.assertTrue(
      Edge((Point(0,1), Point(0,6))).crosses(Edge((Point(0,1), Point(0,5))))
    )
    self.assertTrue(
      Edge((Point(0,0), Point(0,5))).crosses(Edge((Point(0,1), Point(0,5))))
    )
    self.assertTrue(
      Edge((Point(1,0), Point(6,0))).crosses(Edge((Point(1,0), Point(5,0))))
    )
    self.assertTrue(
      Edge((Point(0,0), Point(5,0))).crosses(Edge((Point(1,0), Point(5,0))))
    )

  def test_returns_false_when_colinear_and_fully_contained(self):
    self.assertFalse(
      Edge((Point(0,1), Point(0,4))).crosses(Edge((Point(0,0), Point(0,5))))
    )
    self.assertFalse(
      Edge((Point(1,0), Point(4,0))).crosses(Edge((Point(0,0), Point(5,0))))
    )

  def test_returns_false_when_not_crossing(self):
    self.assertFalse(
      Edge((Point(0,0), Point(0,5))).crosses(Edge((Point(1,3), Point(3,3))))
    )

  def test_returns_true_when_crossing_vertical(self):
    self.assertTrue(
      Edge((Point(0,0), Point(0,5))).crosses(Edge((Point(-3,3), Point(3,3))))
    )

  def test_returns_true_when_crossing_horizontal(self):
    self.assertTrue(
      Edge((Point(-3,3), Point(3,3))).crosses(Edge((Point(0,0), Point(0,5))))
    )

  def test_returns_false_when_crossing_vertical_ends_on_other(self):
    self.assertFalse(
      Edge((Point(0,0), Point(0,5))).crosses(Edge((Point(0,3), Point(3,3))))
    )

  def test_returns_false_when_crossing_ends_on_other(self):
    self.assertFalse(
      Edge((Point(-3,3), Point(3,3))).crosses(Edge((Point(0,0), Point(0,3))))
    )

  def test_returns_false_when_not_crossing_dot(self):
    self.assertFalse(
      Edge((Point(7,1), Point(7,1))).crosses(Edge((Point(9,5), Point(2,5))))
    )