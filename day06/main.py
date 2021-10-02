from collections import defaultdict

with open('day6/input.txt') as f:
   ls = [tuple(s.strip().split(', ')) for s in f.readlines()]

ls = [(int(x[0]),int(x[1])) for x in ls ]

ls.sort()

def closest(p):
   best = 1000
   bestp = None
   two = False
   s = 0
   for q in ls:
      dist = abs(p[0] - q[0]) + abs(p[1] - q[1])
      s += dist
      if dist == best:
         two = True
      if dist < best:
         two = False
         best = dist
         bestp = q
   if two:
      return (None, s)
   return (bestp, s)


totals = defaultdict(int)
inf = set()
region = 0

start = 0
end = 350
for x in range(start, end+1):
   for y in range(start, end+1):
      bestp = closest((x,y))
      totals[bestp[0]] +=1
      if x == end or x == start or y == end or y == start:
         inf.add(bestp[0])
      if bestp[1] < 10000:
         region+=1

newls = []
for p in ls:
   if p not in inf:
      newls.append(totals[p])

newls.sort()
print("Part 1: " + str(newls[-1]))
print("part 2: " + str(region))






#print("Part 1" + str(result))