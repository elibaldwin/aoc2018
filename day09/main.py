input = "403 players; last marble is worth 71920 points"
import math
from collections import deque, defaultdict

def max_score(num_players, num_marbles):
   n = 1
   l = deque([0])
   scores = defaultdict(int)
   while(n <= num_marbles):
      player = n % num_players
      if n % 23 == 0:
         l.rotate(7)
         scores[player] += n + l.pop()
         l.rotate(-1)
      else:
         l.rotate(-1)
         l.append(n)
      n+=1
   return max(scores.values())

pls = 403
pts = 71920

print("Part 1: " + str(max_score(pls, pts)))
print("Part 2: " + str(max_score(pls, pts*100)))
