from math import gcd, floor, sqrt

primes = []
patterns = {2: {0: 6, 1: 2, 2: 4, 3: 8}, 3: {0: 1, 1: 3, 2: 9, 3: 7}, 7: {0: 1, 1: 7, 2: 9, 3: 3}, 9: {0: 1, 1: 9}}

def generate_all_not_coprimes(n):
  if n == 1: return -1
  elif n == 2: return 0
  elif n == 3: return 0
  elif n == 4: return 1
  elif n == 5: return 0
  numbers = [0]*(n - 2)
  q = 0
  for i in range(2, (n>>1) + 1):
    if not numbers[i - 2] and gcd(i, n) != 1:
      for j in range(1, (n-1)//i + 1):
        if not numbers[i * j - 2]:
          numbers[i * j - 2] = 1
          q += 1
  return q

def generate_all_primes(n):
  global primes
  numbers = [0]*(n - 1)
  for i in range(2, floor(sqrt(n)) + 1):
    if not numbers[i - 2]:
      for j in range(i, n//i + 1): numbers[i * j - 2] = 1
  for i in range(len(numbers)):
    if not numbers[i]: primes.append(i + 2)

def prime_exponent_factorial(p, n):
  exponent, denominator = 0, p
  while denominator <= n:
    exponent += n // denominator
    denominator *= p
  return exponent

def prime_decomposition_factorial(n):
  global primes
  dec = {}
  for p in primes:
    if p > n: return dec
    dec[p] = prime_exponent_factorial(p, n)
  return dec

def comb_last_digit(q, k):
  global patterns
  generate_all_primes(q)
  q_dec = prime_decomposition_factorial(q)
  k_dec = prime_decomposition_factorial(k)
  q_k_dec = prime_decomposition_factorial(q - k)
  for key, value in k_dec.items(): q_dec[key] -= value
  for key, value in q_k_dec.items(): q_dec[key] -= value
  if q >= 5:
    if q_dec[2] >= q_dec[5]: q_dec[2], q_dec[5] = q_dec[2] - q_dec[5], 0
    else: q_dec[2], q_dec[5] = 0, q_dec[5] - q_dec[2]
  result = 1
  for key, value in q_dec.items():
    if value and key == 2: result *= patterns[2][value % 4]
    elif value and (key % 10 == 3): result *= patterns[3][value % 4]
    elif value and (key == 5): result *= 5
    elif value and (key % 10 == 7): result *= patterns[7][value % 4]
    elif value and (key % 10 == 9): result *= patterns[9][value % 2]
  return result % 10

if __name__ == "__main__":
  n, k = list(map(int, input().strip().split(" ")))
  q = n - 1 - generate_all_not_coprimes(n)
  if q == 0 or k > q: print(-1)
  elif q == 1 and k == 1: print(1)
  elif q == 1: print(-1)
  else:
    result = comb_last_digit(q, k)
    print(result)