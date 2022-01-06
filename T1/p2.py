# https://www.geeksforgeeks.org/iterative-merge-sort/
# https://www.geeksforgeeks.org/maximum-distance-between-two-points-in-coordinate-plane-using-rotating-calipers-method/
# https://www.geeksforgeeks.org/fast-i-o-for-competitive-programming-in-python/

from io import BytesIO
from os import fstat, read

class Point:
  def __init__(self, x = None, y = None):
    self.x = x
    self.y = y
  def __repr__(self):
    return "(" + str(self.x) + ", " + str(self.y) + ")"

def gain(p1, p2):
  g = (p2.x - p1.x) * (p2.y - p1.y + 1)
  max = 0
  if g > max and p2.x > p1.x and p2.y >= p1.y: max = g
  return max

def distSq(p1, p2):
    return ((p1.x - p2.x) * (p1.x - p2.x) + (p1.y - p2.y) * (p1.y - p2.y))

def absArea(p, q, r):
  a = (p.y - q.y) * (q.x - r.x) - (q.y - r.y) * (p.x - q.x)
  if a < 0: return a * -1
  else: return a

def orientation(pivot, q, r):
  val = ((q.y - pivot.y) * (r.x - q.x) - (q.x - pivot.x) * (r.y - q.y))
  if val == 0:
    return 0  # collinear
  elif val > 0:
    return 1  # clock wise
  else:
    return 2  # counterclock wise
  
def compare(pivot, p1, p2): # 1 significa que p2 es "mas grande"
    o = orientation(pivot, p1, p2)
    if o == 0:
        if distSq(pivot, p2) >= distSq(pivot, p1): return 1
        else: return 0
    else:
        if o == 2: return 1
        else: return 0

def merge_sort(dots, pivot):
  curr_size = 1
  while (curr_size <= len(dots) - 1):
    left_start = 0
    while (left_start < len(dots) - 1):
      mid = min(left_start + curr_size - 1, len(dots) - 1)
      right_end = min(left_start + 2*curr_size - 1, len(dots) - 1)
      merge(dots, left_start, mid, right_end, pivot)
      left_start += 2*curr_size
    curr_size = 2*curr_size
  return dots

def merge(dots, l, m, r, pivot):
  n1, n2 = m - l + 1, r - m
  L, R = [0] * n1, [0] * n2
  for i in range(0, n1):
    L[i] = dots[l + i]
  for i in range(0, n2):
    R[i] = dots[m + i + 1]
  i, j, k = 0, 0, l
  while i < n1 and j < n2:
    if compare(pivot, R[j], L[i]):
      dots[k] = R[j]
      j += 1
    else:
      dots[k] = L[i]
      i += 1
    k += 1
  while i < n1:
    dots[k] = L[i]
    i += 1
    k += 1
  while j < n2:
    dots[k] = R[j]
    j += 1
    k += 1

def convexHull(points):
  ymin = points[0].y
  min = 0
  for i in range(1, len(points)):
    y = points[i].y
    if ((y < ymin) or (ymin == y and points[i].x < points[min].x)):
      ymin = points[i].y
      min = i
  points[0], points[min] = points[min], points[0]
  pivot = points[0]
  points = merge_sort(points, pivot)
  size = 1
  i = 1
  while i < len(points):
    while ((i < len(points) - 1) and (orientation(pivot, points[i], points[i + 1]) == 0)):
      i += 1
    points[size] = points[i]
    size += 1
    i += 1
  points = points[:size]
  if size < 3:
    return points
  S = []
  S.append(points[0])
  S.append(points[1])
  S.append(points[2])
  for i in range(3, size):
    while ((len(S) > 1) and (orientation(S[-2], S[-1], points[i]) != 2)):
      S.pop()
    S.append(points[i])
  return S

def rotatingCaliper(producers, buyers):
  ph = convexHull(producers)
  bh = convexHull(buyers)
  k = 1
  res = 0
  if len(ph) == 1:
    for p in bh:
      res = max(res, gain(ph[0], p))
  elif len(bh) == 1:
    for p in ph:
      res = max(res, gain(p, bh[0]))
  while (k < len(bh) and gain(ph[0], bh[(k + 1) % len(bh)]) > gain(ph[0], bh[k])):
    k += 1
  i, j = 0, k
  while i < len(ph) and j < len(bh):
    res = max(res, gain(ph[i], bh[j]))
    while (j < len(bh) and gain(ph[i], bh[(j + 1) % len(bh)]) > gain(ph[i], bh[(j + 1) % len(bh)])):
      res = max(res, gain(ph[i], bh[(j + 1) % len(bh)]))
      j += 1
    i += 1
  return res

if __name__ == "__main__":
  input = BytesIO(read(0, fstat(0).st_size)).readline
  producers = []
  buyers = []
  m, n = list(map(int, input().decode().strip().split(" ")))
  for _ in range(m):
    x, y = list(map(int, input().decode().strip().split(" ")))
    producers.append(Point(x, y))
  for _ in range(n):
    x, y = list(map(int, input().decode().strip().split(" ")))
    buyers.append(Point(x, y))
  if m == 1:
    max = 0
    for b in buyers:
      d = gain(producers[0], b)
      if d > max: max = d
    print(max)
  elif n == 1:
    max = 0
    for p in producers:
      d = gain(p, buyers[0])
      if d > max: max = d
    print(max)
  elif m < 100 and n < 100:
    max = 0
    for p in producers:
      for b in buyers:
        d = gain(p, b)
        if d > max: max = d
    print(max)
  else:
    print(rotatingCaliper(producers, buyers))