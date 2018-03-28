import os
from field import Field


def player_steps(way):
  for step in way:
    yield step


class PlayGround(object):
  def __init__(self):
    self.players = []

  def clear(self):
    os.system('clear')

  def add_field(self, rows, cols, lets = []):
    self.field = Field(rows, cols)
    for r, c in lets:
      self.field.add_let(r*cols+c)

  def add_player(self, position, destination, label = 'X'):
    p_r, p_c = position
    d_r, d_c = destination
    from_node = p_r*self.field.cols+p_c
    to_node = d_r*self.field.cols+d_c
    self.players.append(dict(
      label = label,
      position = from_node,
      destination = to_node,
      way = player_steps(self.field.way(from_node, to_node)[1:]),
    ))

  def play_step(self):
    complete_players = 0
    player_stop = False
    while True:
      if complete_players==len(self.players): break
      complete_players = 0
      for player in self.players:
        if player['position'] == player['destination']: complete_players+=1; continue
        new_position = player['way'].__next__()
        if new_position in self.field.players:
          seen_positions = list(self.field.players)
          seen_positions.remove(player['position'])
          print('Player %s find the LET'%player['label'])
          print('Try to find new way for player %s'%player['label'])
          print(player['position'], player['destination'], seen_positions)
          print(self.field.way(player['position'], player['destination'], seen_positions))
          player['way'] = player_steps(self.field.way(player['position'], player['destination'], seen_positions)[1:])
          new_position = player['way'].__next__()
        player['position'] = new_position
        yield str(self)

  def __str__(self):
    self.field.add_players({player['position']: player['label'] for player in self.players})
    return str(self.field)

