# https://www.geeksforgeeks.org/find-the-number-of-paths-of-length-k-in-a-directed-graph/
# Se obtuvo la idea del codigo citado.
# Esto es, el uso de exponenciación de matrices y exponenciación cuadrática para la complejidad terórica con operaciones O(1)
# Se reimplemento de forma iterativa, concisa y aplicada al problema
# Se utilizan propiedades modulares para mantener la multiplicación de enteros en O(1)

A = [[0, 2, 2, 1], [2, 0, 0, 1], [2, 0, 0, 1], [1, 1, 1, 0]]
resp = A

def multiply(a, b):
  global resp
  t = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
  for i in range(4):
    for j in range(4):
      for k in range(4):
        t[i][j] += a[i][k] * b[k][j]
      t[i][j] = t[i][j] % (10**9 + 7)
  resp = t

if __name__ == "__main__":
  N = int(input("Inserte el N: "))
  # N = 100000000000000000000000
  # print("N:", N)
  if N == 0:
    print(4)
  else:
    Ns = []
    while N > 1:
      Ns.append(N)
      N //= 2
    for n in reversed(Ns):
      multiply(resp, resp)
      if (n % 2 != 0):
        multiply(resp, A)
    print((((resp[0][1] + resp[0][2] + resp[0][3] + resp[1][2] + resp[1][3] + resp[2][3]) * 2) + resp[0][0] + resp[1][1] + resp[2][2] + resp[3][3]) % (10**9 + 7))