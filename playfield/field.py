from dijkstra import dijkstra
from collections import defaultdict

const_char = 'abcdefghijklmnopqrstuvwxyz'.upper()


# class Way(object):
#   def __init__(self, way):
#     self.way = way[1:]
#
#   def play(self):
#     for step in self.way:
#       yield step


def player_step(way):
  for step in way:
    yield step


class Field(object):
  def __init__(self, rows, cols):
    self.players = []
    self.rows=rows if rows<=10 else 10
    self.cols=cols if cols<=10 else 10
    self.make()

  def make(self):
    nodes = defaultdict(list)
    for r in range(self.rows):
      for c in range(self.cols):
        node = self.rows*r+c
        n_nodes = self.get_neigtbor_nodes(node,r,c)
        nodes[node].extend(n_nodes)
        for n_node in n_nodes: nodes[n_node].append(node)
    self.nodes = nodes

  def get_neigtbor_nodes(self,index,r,c):
    nodes = []
    if c > 0:
      nodes.append(index - 1)
    if r > 0:
      nodes.append(index - self.cols)
      if c == 0:
        nodes.append(index - self.cols + 1)
      elif c == self.cols - 1:
        nodes.append(index - self.cols - 1)
      else:
        nodes.append(index - self.cols + 1)
        nodes.append(index - self.cols - 1)
    return [node for node in nodes if node>=0]

  def way(self, from_node, to_node, seen_nodes = []):
    edges = []
    for node, n_nodes in self.nodes.items():
      for n_node in n_nodes:
        edges.append((node, n_node, 1))
    way = dijkstra(edges, from_node, to_node, seen_nodes)
    return way

  def delete_node(self, node):
    for n_node in self.nodes[node]:
      self.nodes[n_node].remove(node)
    del self.nodes[node]

  def add_player(self, label, from_node, to_node):
    self.players.append(dict(
      label = label,
      position = from_node,
      destination = to_node,
      way = player_step(self.way(from_node, to_node)[1:])
    ))

  def step(self):
    for player in self.players:
      new_position = player['way'].__next__()
      # TODO: check new position
      player['position'] = new_position

  def __str__(self):
    """
    :return:
           0   1   2
         ------------- # row_delimiter
      A  |   | o |   | #
         -------------
      B  |   |   |   |
         -------------
      C  |   |   | o |
         -------------
    """
    tab = " "*5
    player_positions = {player["position"]: player["label"] for player in self.players}
    row_delimiter = lambda cols: '-'*(cols*4+1)+'\n'
    str_field = ""
    str_field+=tab+"".join(["  %s "%col for col in range(self.cols)])+"\n"
    str_field+=tab+row_delimiter(self.cols)
    for row in range(self.rows):
      str_field+='  %s  |'%const_char[row]
      for col in range(self.cols):
        node = self.rows*row+col
        if not node in self.nodes: cell='X'
        elif node in player_positions: cell=player_positions[node]
        else: cell = ' '
        str_field+=' %s |'%cell
      str_field+='\n'+tab+row_delimiter(self.cols)
    return str_field