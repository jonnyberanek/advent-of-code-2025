from dataclasses import dataclass
from typing import Any, NamedTuple, Self

PUZZLE_1_EXPECTS = 21
PUZZLE_2_EXPECTS = 40

class Point(NamedTuple):
  x: int
  y: int

@dataclass
class BeamNode:
  pos: Point # For easier coding, maybe not the best practice
  left: Self | None = None
  right: Self | None = None

  def __hash__(self) -> int:
    return id(self)

class ManifoldBuilder:
  root: BeamNode | None = None
  graph: dict[Point, BeamNode] = {}

  y_index_by_x: dict[int, list[int]] = {}

  def add(self, pos: Point):
    if pos.x not in self.y_index_by_x:
      self.y_index_by_x[pos.x] = []
    self.y_index_by_x[pos.x].append(pos.y)

    node = BeamNode(pos)
    self.graph[pos] = node
    return node

  def build_connected_tree(self, root: BeamNode) -> BeamNode:
    self.connected_nodes = set()

    self.__build_manifold_node(root)

    return root

  def __build_manifold_node(self, node: BeamNode):
    # optimization for nodes that already were discovered
    if node.left or node.right:
      return
    
    left_hit = self.__find_beam_hit(node.pos.x - 1, node.pos.y)
    right_hit = self.__find_beam_hit(node.pos.x + 1, node.pos.y)

    if left_hit:
      node.left = self.graph[left_hit]
      self.__build_manifold_node(node.left)

    if right_hit:
      node.right = self.graph[right_hit]
      self.__build_manifold_node(node.right)

  def __find_beam_hit(self, x, origin_y):
    if x not in self.y_index_by_x:
      return None
        
    all_line = self.y_index_by_x[x]

    next_y = None
    
    for y in all_line:
      if y > origin_y:
        next_y = y
        break
    
    if not next_y:
      return None
    
    return Point(x, next_y)

def parse_manifold(input: list[str]) -> BeamNode:

  manifold = ManifoldBuilder()
  root: BeamNode | None = None

  for y, line in enumerate(input):
    for x, char in enumerate(line):
      if char == "^":
        node = manifold.add(Point(x,y))
        # we can assume the first node found is the root
        if not root:
          root = node

  if not root:
    raise Exception()

  return manifold.build_connected_tree(root)
    

def solve_puzzle_1(input: list[str]) -> Any:

  def discover_tree(node: BeamNode, connected_nodes: set[BeamNode]):
    if node in connected_nodes: # optimization so this actually runs fast
      return connected_nodes

    connected_nodes.add(node)

    if node.left:
      discover_tree(node.left, connected_nodes)
    if node.right:
      discover_tree(node.right, connected_nodes)
    
    return connected_nodes

  return len(discover_tree(parse_manifold(input), set()))


      
@dataclass
class Box[T]:
  value: T

def solve_puzzle_2(input: list[str]) -> Any:
  # Keeps track of nodes whose path total have already be calculated
  # Needs to be done this way to optimize not going down every single path
  count_cache = dict[Point, int]()

  def find_path_count(node: BeamNode):
    if node.pos in count_cache: 
      return count_cache[node.pos]
    
    value = 0
    if not node.left:
      value += 1
    else:
      value += find_path_count(node.left)

    if not node.right:
      value += 1
    else:
      value += find_path_count(node.right)

    count_cache[node.pos] = value
    return value

  return find_path_count(parse_manifold(input))  

