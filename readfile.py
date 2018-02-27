# Чтение данных из файла

import sys


def get_data():
  """
  Парсит данные из файла в числовые значения
  :return: список числовых значений
  """
  if len(sys.argv)!=2: return None
  file_name = sys.argv[1]
  res = []
  try:
    with open(file_name, 'r') as f:
      for line in f:
        res.append([float(value) for value in line.split()])
  except IOError as err:
    print(err)
    return None
  except ValueError as err:
    print(err)
    return None
  return res


if __name__=="__main__":
  print(get_data())