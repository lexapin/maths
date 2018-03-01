# Расчет системы алгебраических уравнений методом Гаусса
# В задании не было сказано каким метоодом решать уравнение
# Поэтому мной был выбран итерационный метод Гаусса-Зейделя
# У данного метода есть проблемы с обусловленностью матриц
# Поэтому на мощных тестах врядли метод адекватно решит матрицу
# Суть метода в том, чтобы на каждой итерации находить новое приближение
# X(n+1) = D^-1 * [ b - ( L + H ) * Xn ]
# где
# AX = b
# A = L + D + H
# L      - треугольная матрица ниже диагонали
# D      - диагональная матрица
# H      - треугольная матрица выше диагонали
# Xn     - начальное приближение для X
# X(n+1) - следующее приближение для X
#
# Затрачено времени: 40 минут

from copy import deepcopy
from math import fabs as abs

# Дефолтные значения если в аргументах файл не задан:
# Матрица коэффициентов A
global_A = [
  [ 3, -1, -1,  0,],
  [-1,  2,  0,  0,],
  [-1,  0,  2, -1,],
  [ 0,  0, -1,  1,],
]

# Матрица-вектор b
global_b = [1, 1, 1, 1,]

# Начальное приближение X
global_X = [2, 2, 4, 5,]


def split_matrix(A):
  """
  Функция делит матрицу A на рабочие матрицы D^-1 и L+H
  """
  matrix_D = []
  matrix_LH = deepcopy(A)
  for i in range(len(A)):
    matrix_D.append(1/A[i][i])
    matrix_LH[i][i] = 0
  return matrix_D, matrix_LH


def multiplyM(Matrix, Vector):
  """
  Функция умножения матрицы на вектор
  """
  res = []
  for i in range(len(Matrix)):
    sum = 0
    for j in range(len(Vector)):
      sum+=Matrix[i][j]*Vector[j]
    res.append(sum)
  return res


def multiplyD(DIAG, Vector):
  """
  Функция умножения диагональной матрицы на вектор
  """
  return [DIAG[i]*Vector[i] for i in range(len(Vector))]


def minus(v1, v2):
  """
  функция вычитания двух векторов
  """
  return [v1[i]-v2[i] for i in range(len(v1))]


def delta(curr_v, next_v):
  """
  Функция вычисления суммарной невязки между текукщим и следующим значением X
  """
  return sum([abs(curr_v[i]-next_v[i]) for i in range(len(curr_v))])


def linear(A, X, b, sigma=0.001, max_iter = 100):
  """
  Основная функция для решения системы линейных уравнений метоодом Гауса-Зейделя
  """
  curr_v = X
  D, LH = split_matrix(A)
  iteration = 0
  while True:
    next_v = multiplyD(D,minus(b, multiplyM(LH,curr_v)))
    if delta(next_v, curr_v)<sigma: break
    curr_v = next_v
    if iteration>max_iter: break
    iteration+=1
  return next_v

if __name__=="__main__":
  from readfile import get_data
  data = get_data()
  if data is None:
    A = global_A
    X = global_X
    b = global_b
  else:
    A = data[:-2]
    X = data[-1]
    b = data[-2]
  print(linear(A,X,b))
