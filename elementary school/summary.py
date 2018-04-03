import os, sys, random


def clear():
  os.system('cls' if os.name == 'nt' else 'clear')


def set_digit():
  sys.stdout.write('\nВыбери, с какими цифрами будем работать?\n')
  sys.stdout.write(', '.join([str(i) for i in range(2, 10)]))
  sys.stdout.write('?\n')
  total_tries = 3
  current_try = 1
  digit = 0
  while True:
    if current_try > total_tries: break
    current_try+=1
    data = sys.stdin.readline()
    try:
      digit = int(data)
      if digit > 20: raise ValueError
      return digit
    except ValueError:
      sys.stdout.write('Я не понял число. Введи число еще раз!\n')
      continue
  clear()
  sys.stdout.write('Я запутался. Открой меня еще раз\n')
  sys.exit(0)


def test(digit):
  clear()
  total = 0
  right = 0
  for i in range(digit):
    for j in range(3):
      total+=1
      d1 = random.randint(1, digit)
      sys.stdout.write('%s + %s = ?\n'%(i, d1))
      right_answer = str(i+d1)
      user_answer = sys.stdin.readline()[:-1]
      # print(user_answer, type(user_answer))
      if user_answer==right_answer: sys.stdout.write('Правильно. Молодец! Пойдем дальше.\n'); right+=1
      else: sys.stdout.write('Ой. Ошибочка. Правильный ответ %s. Хорошенько подумай над следующим примером.\n'%right_answer)
      sys.stdin.readline()
      clear()
  return right, total


def main():
  clear()
  sys.stdout.write('ПРИВЕТ КОЛЯ, ПОЗАНИМАЕМСЯ МАТЕМАТИКОЙ?')
  digit = set_digit()
  sys.stdout.write('Начнем, Коля. Нажми кнопку ENTER\n')
  sys.stdin.readline()
  right, total = test(digit)
  sys.stdout.write('Вот и закончился наш тест, Коля\n')
  sys.stdout.write('Ты справился с %s примерами из %s. Неплохо! Потренируйся еще раз - запусти меня снова!\n'%(right, total))
  sys.stdin.readline()
  sys.exit(0)


if __name__ == '__main__':
  main()