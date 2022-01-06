from random import randint
from math import gcd, log2
from time import time

def es_potencia(n: int):
  if n <= 3: return False
  for k in range(2, int(log2(n)) + 1):
    if tiene_raiz_entera(n, k): return True
  return False

def tiene_raiz_entera(n: int, k: int):
  if n <= 3: return False
  a = 1
  while pow(a,k) < n: a <<= 1
  return tiene_raiz_entera_intervalo(n, k, a>>1, a)

def tiene_raiz_entera_intervalo(n: int, k: int, i: int, j: int):
  while i <= j:
    if i==j: return n == pow(i,k)
    p = (i + j)>>1
    val = pow(p,k)
    if n == val: return True
    elif val < n: i = p+1
    else: j = p-1
  return False

def primality(n, k):
  if n == 1: return False
  elif n == 2: return True
  elif n%2 == 0: return False
  elif es_potencia(n): return False
  else:
    neg = 0
    for _ in range(1, k+1):
      a = randint(2, n-1)
      if gcd(a, n) > 1: return False
      else:
        b = pow(a, (n-1)>>1, n)
        if b == n - 1: neg = neg + 1
        elif b != 1: return False
    if neg > 0: return True
    else: return False

def fast_primality(n: int):
  if n == 1: return False
  elif n == 2: return True
  elif n%2 == 0: return False
  else:
    neg = 0
    for _ in range(1, 15+1):
      a = randint(2, n-1)
      if gcd(a, n) > 1: return False
      else:
        b = pow(a, (n-1)>>1, n)
        if b == n - 1: neg = neg + 1
        elif b != 1: return False
    if neg > 0: return True
    else: return False

def generar_primo(a, b):
  if a == b and primality(a, 100): return a
  elif a == b: return -1
  if a%2 == 0: a += 1
  if a == b and primality(a, 100): return a
  elif a == b: return -1
  if b%2 == 0: b -= 1
  if a == b and primality(a, 100): return a
  elif a == b: return -1
  if primality(a, 100): return a
  if primality(b, 100): return b
  init = time()
  selected = set()
  selected.add(a)
  selected.add(b)
  candidates = b - a + 1
  for _ in range(400000):
    elem = randint(a, b)
    if elem not in selected and fast_primality(elem) and primality(elem, 100): return elem
    selected.add(elem)
    if candidates == len(selected): return -1
    if time() - init > 1.8: return -1
  return -1

if __name__ == "__main__":
  a, b = list(map(int, input().strip().split(" ")))
  print(generar_primo(a, b))