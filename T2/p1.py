from cmath import pi, exp
from collections import defaultdict
from math import log2

# memory for the fft
w = defaultdict(lambda: None)

# FFT as saw in class
def FFT(polynomial):
  n = len(polynomial)
  if n == 2:
    a0, a1 = polynomial[0], polynomial[1] 
    return [a0 + a1, a0 - a1]
  else:
    y = [0]*n
    polynomial0 = y[:(n >> 1)]
    polynomial1 = y[:(n >> 1)]
    for i in range(n):
      if i%2: polynomial1[i >> 1] = polynomial[i]
      else: polynomial0[i >> 1] = polynomial[i]
    y0, y1 = FFT(polynomial0), FFT(polynomial1)
    if not w[n]: # if there are w values in the memory for the n length
      w[n] = dict()
      w[n][0] = 1
      wn = exp(pi * 2j / n)
      for k in range(n >> 1):
        w[n][k + 1] = w[n][k] * wn
    for k in range(n >> 1):
      a0 = y0[k]
      a1 = w[n][k] * y1[k]
      y[k], y[(n >> 1) + k] = a0 + a1, a0 - a1
    return y

if __name__ == "__main__":
  s, t, k = list(map(int, input().strip().split(" ")))
  S = input().strip()
  T = input().strip()[::-1]
  vector_length = 2 << int(log2(s + t - 1) // 1)
  template = [0] * vector_length
  total = template[:]
  for char in "ACGT":
    S_vector, T_vector, pivot = template[:], template[:], -1
    for i in range(t): T_vector[i] = 1 if T[i] == char else 0
    # k-lookahead automata
    for i in range(min(k + 1, s)): 
      if S[i] == char: pivot = i
    for i in range(s):
      if pivot >= 0 and pivot - k <= i and i <= pivot + k: S_vector[i] = 1
      if k + i + 1 < s and S[i + k + 1] == char: pivot = k + i + 1
    # Convolution
    y1, y2 = FFT(T_vector), FFT(S_vector)
    y = [a1 * a2 for a1, a2 in zip(y1, y2)]
    y0 = FFT([y[0]] + y[:0:-1])
    for i in range(vector_length): total[i] += round(y0[i].real / vector_length)
  print(sum(1 for i in range(s) if total[i] == t))