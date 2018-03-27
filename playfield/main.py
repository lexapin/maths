import sys
from field import Field


def player_step(way):
  for step in way:
    yield step


def main():
  field = Field(rows=5, cols=5)
  field.delete_node(12)
  field.delete_node(16)
  field.delete_node(17)
  sys.stdout.write(str(field))
  way = field.way(23,6)
  print(way)
  field.add_player('A', 23, 6)
  sys.stdout.write('\n')
  sys.stdout.write(str(field))
  while True:
    try:
      field.step()
    except StopIteration:
      break
    sys.stdout.write('\n')
    sys.stdout.write(str(field))

if __name__ == '__main__':
  main()