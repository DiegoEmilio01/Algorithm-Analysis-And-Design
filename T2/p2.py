# code based on https://codeforces.com/contest/1523/submission/133691213
from io import BytesIO
from os import fstat, read
from random import choice
from collections import Counter


if __name__ == "__main__":
  input = BytesIO(read(0, fstat(0).st_size)).readline
  n, m, p = list(map(int, input().decode().strip().split(" ")))
  people = []
  for i in range(n):
    people.append(int(input(), 2))
  best = (0, 0)
  for _ in range(10):
    # choose a candidate, the candidate represents the group. Is it a good representant due there are more than n/2 of them
    curr_person = choice(people)
    # generates compatibility between a candidate and the rest of them
    common_coins, common_coins2, person = dict(Counter((person & curr_person for person in people))), {}, curr_person
    # generates the posible answers given a candidate (all the subsets)
    while person > 0:
      common_coins2[person], person = 0, (person - 1) & curr_person
    # for every compatibility generates ans and add the appearance frequencies to the previously calculated ans
    for coins in common_coins.keys():
      person = coins
      while person > 0:
        common_coins2[person] += common_coins[coins]
        person = (person - 1) & coins
    # for every answer that satisfy the n/2 condition calculates the best
    for person, freq in common_coins2.items():
      if freq >= (n+1)//2: best = max(best, (bin(person).count("1"), person))
  print("{{:0{}b}}".format(m).format(best[1]))
 
