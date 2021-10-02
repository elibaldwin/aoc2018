with open('input.txt') as f:
   ls = [s.strip() for s in f.readlines()]

import parse

pr = parse.compile('pos=<{:d},{:d},{:d}>, r={:d}')

bots = []

for l in ls:
   r = pr.parse(l)
   bots.append((r[0],r[1],r[2],r[3]))

from Queue import PriorityQueue

q = PriorityQueue()

for x,y,z,r in bots:
  d = abs(x) + abs(y) + abs(z)
  q.put((max(0, d - r),1))
  q.put((d + r,-1))
count = 0
maxCount = 0
result = 0
while not q.empty():
  dist,e = q.get()
  count += e
  if count > maxCount:
    result = dist
    maxCount = count
print(result)