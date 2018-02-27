# Расчет коэфициентов интерполяционного полинома Лагранжа
# Данный полином строится по следующей формуле:
#          n
#  Ln(x) = ∑li(x)*yi  (1)
#         i=0
#
# где
# li(x) - искомые коэффициенты Лагранжа
# yi    - значение функции в точке xi
#
# для дискретной функции yi = f(xi) коэффициенты
# определяются следующим образом:
#           n
#   li(x) = ∏(x-xj)/(xi-xj)  (2)
#        j=0,j≠i
#
# Подставляя (2) в (1) вычисляется искомый полином
# Затрачено времени: 50 минут


from operator import mul as multiply_list
from functools import reduce

# Значения по умолчанию
x_global = [-2, -1, -1.2, 3.5, 5,]
y_global = [-4,  0,  3.8,  -2, 7,]


class LagrKoef(object):
  """

  """
  def __init__(self, mn = 0, *args):
    """
    Заполняем аргументы
    :param mn: расчитанный множитель
    :param args: аргументы xi для постановвки в многочлен
    """
    self.mn = mn
    self.args = args

  def __call__(self, x_value):
    """
    Вычисление коэффициента
    :param x_value: значение x
    :return: Коэффициент Лагранжа для x
    """
    return reduce(multiply_list, [x_value-arg for arg in self.args], 1) * self.mn

  def __repr__(self):
    """
    Для отладки
    :return: Множитель и коэффициенты
    """
    return "LK: mn=%s, keofs=%s"%(self.mn, self.args)


def find_lang_koefs(x_list, y_list):
  """
  Функция расчета коэффициентов Лагранжа по формуле (2)
  Совмещая частично с формулой 1
  :param x_list: значения xi искомой дискретной функции
  :param y_list: значения yi искомой дискретной функции
  :return: Список коэффициентов Лагранжа
  """
  koefs = []
  for i in range(len(y_list)):
    mn = y_list[i]/reduce(
        multiply_list,
        [x_list[i]-x_list[j] for j in range(len(x_list)) if i!=j],
        1
    )
    mod_x = [x_list[j] for j in range(len(x_list)) if i!=j]
    koefs.append(LagrKoef(mn, *mod_x))
  return koefs


def solve_polinom(koefs, x_value):
  """
  Вычисляет значение интерполянта в точке x
  :param koefs: коэффициенты Лагранжа
  :param x_value: значение точки x
  :return:
  """
  return sum([koef(x_value) for koef in koefs])


if __name__=="__main__":
  from readfile import get_data
  data = get_data()
  x, y = x_global, y_global if data is None else data
  koefs = find_lang_koefs(x, y)
  for koef in koefs: print(koef)
  print(solve_polinom(koefs, -1))