import sys
from playground import PlayGround


def test1():
  """
  field 6x6
  four players
  :return:
  """
  pg = PlayGround()
  pg.clear()
  pg.add_field(6, 6)
  pg.add_player((0,0), (5,5), 'A')
  pg.add_player((5,5), (0,0), 'B')
  pg.add_player((0,5), (5,0), 'C')
  pg.add_player((5,0), (0,5), 'D')
  str_data = str(pg)
  str_data+='\nTest 1\nField 6x6\n'
  str_data+='Player A: start_position A0, destination_position F5\n'
  str_data+='Player B: start_position F5, destination_position A0\n'
  str_data+='Player A: start_position A5, destination_position F0\n'
  str_data+='Player B: start_position F0, destination_position A5\n'
  print(str_data)
  for step in pg.play_step():
    sys.stdin.readline()
    pg.clear()
    print(step)
  print("Test 1 complete.\n")
  sys.stdin.readline()


def test2():
  """
  field 5x5
  two players
  three barriers
  :return:
  """
  pg = PlayGround()
  pg.clear()
  pg.add_field(5,5,[(3,1), (3,2), (2,2)])
  pg.add_player((4,3), (1,1), 'A')
  pg.add_player((1,1), (4,3), 'B')
  str_data = str(pg)
  str_data+='\nTest 2\nField 5x5\n'
  str_data+='Player A: start_position E3, destination_position B1\n'
  str_data+='Player B: start_position B1, destination_position E3\n'
  str_data+='Bariers: C2, D1, D2\n'
  print(str_data)
  for step in pg.play_step():
    sys.stdin.readline()
    pg.clear()
    print(step)
  print("Test 2 complete.\n")
  sys.stdin.readline()


def test3():
  """
  field 5x10
  four players
  six barriers
  :return:
  """
  pg = PlayGround()
  pg.clear()
  pg.add_field(5,10,[(3,1), (3,2), (2,2), (1,6), (2,6), (3,6)])
  pg.add_player((4,3), (1,1), 'A')
  pg.add_player((1,1), (4,3), 'B')
  pg.add_player((1,7), (4,0), 'C')
  pg.add_player((4,8), (0,0), 'D')
  str_data = str(pg)
  str_data+='\nTest 3\nField 5x10\n'
  str_data+='Player A: start_position E3, destination_position B1\n'
  str_data+='Player B: start_position B1, destination_position E3\n'
  str_data+='Player C: start_position B7, destination_position E0\n'
  str_data+='Player D: start_position E8, destination_position A0\n'
  str_data+='Bariers: C2, D1, D2\n'
  print(str_data)
  for step in pg.play_step():
    sys.stdin.readline()
    pg.clear()
    print(step)
  print("Test 3 complete.\n")
  sys.stdin.readline()


def main():
  test1()
  test2()
  test3()

if __name__ == '__main__':
  main()