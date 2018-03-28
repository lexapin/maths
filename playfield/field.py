from dijkstra import dijkstra
from collections import defaultdict

const_char = 'abcdefghijklmnopqrstuvwxyz'.upper()


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
        node = self.cols*r+c
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

  def add_let(self, node):
    for n_node in self.nodes[node]:
      self.nodes[n_node].remove(node)
    del self.nodes[node]

  def add_players(self, players):
    self.players = players

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
    row_delimiter = lambda cols: '-'*(cols*4+1)+'\n'
    str_field = ""
    str_field+=tab+"".join(["  %s "%col for col in range(self.cols)])+"\n"
    str_field+=tab+row_delimiter(self.cols)
    for row in range(self.rows):
      str_field+='  %s  |'%const_char[row]
      for col in range(self.cols):
        node = self.cols*row+col
        if not node in self.nodes: cell='X'
        elif node in self.players: cell=self.players[node]
        else: cell = ' '
        str_field+=' %s |'%cell
      str_field+='\n'+tab+row_delimiter(self.cols)
    return str_field