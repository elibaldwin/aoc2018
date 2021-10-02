with open('day10/input.txt') as f:
   ls = [s.strip() for s in f.readlines()]

import parse

points = []
pr = parse.compile("position=<{}, {}> velocity=<{}, {}>")

for l in ls:
   r = pr.parse(l)
   point = [r[0], r[1], r[2], r[3]]
   points.append([int(x) for x in point])

def inc(ps):
   for p in ps:
      p[0] += p[2]
      p[1] += p[3]

def mins(ps):
   minx = 1000
   miny = 1000
   maxx = -1000
   maxy = -1000
   for p in ps:
      minx = min(minx, p[0])
      miny = min(miny, p[1])
      maxx = max(maxx, p[0])
      maxy = max(maxy, p[1])
   return ((minx, miny), (maxx, maxy))

def height(ps):
   ms = mins(ps)
   return ms[1][1] - ms[0][1]

inccount = 0
while(height(points) > 10):
   inc(points)
   inccount += 1

ms = mins(points)

grid = [['.' for _ in range(ms[1][0] - ms[0][0] + 1)] for _ in range(height(points) + 1)]

for p in points:
   transx = p[0] - ms[0][0]
   transy = p[1] - ms[0][1]
   grid[transy][transx] = '#'

for r in grid:
   print(''.join(r))

print(inccount)

