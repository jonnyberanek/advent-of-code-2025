import itertools
from typing import Any

from day09.geometry import Point, Polygon
from util.logger import logger
from util.functions import multiply

PUZZLE_1_EXPECTS = 50
PUZZLE_2_EXPECTS = 24

def parse_red_tiles(input: list[str]) -> list[Point]:
  return [Point(*(int(c) for c in line.split(","))) for line in input]

def solve_puzzle_1(input: list[str]) -> Any:
  red_tiles = parse_red_tiles(input)

  max_area = 0
  # combinations to avoid double checks
  for tile1, tile2 in itertools.combinations(red_tiles, 2):
    area = multiply( *( abs(tile1[i] - tile2[i]) + 1 for i in range(len(tile1)) ) )
    if area > max_area:
      max_area = area

  return max_area


def solve_puzzle_2(input: list[str]) -> Any:
  tile_polygon = Polygon(parse_red_tiles(input))

  def is_valid_rect(rect: Polygon):
    for rect_edge in rect.get_edges():
      for polygon_edge in tile_polygon.get_edges():
        if rect_edge.crosses(polygon_edge):
          logger.t(f"{rect_edge} crosses {polygon_edge}")
          return False
    return True

  max_area = 0
  maxes = None
  # combinations to avoid double checks
  for tile1, tile2 in itertools.combinations(tile_polygon, 2):
    rect = Polygon([tile1, Point(tile1.x, tile2.y), tile2, Point(tile2.x, tile1.y)])

    if not is_valid_rect(rect):
      continue

    area = multiply( *( abs(tile1[i] - tile2[i]) + 1 for i in range(len(tile1)) ) )
    logger.t(f"valid rect of {tile1} x {tile2}. Area: {area}")
    if area > max_area:
      max_area = area
      maxes = (tile1, tile2)

  logger.v(maxes)

  return max_area


