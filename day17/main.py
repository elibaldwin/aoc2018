with open('input.txt') as f:
   ls = [s.strip() for s in f.readlines()]

boxes = []

import parse

pr = parse.compile('x={:d}, y={:d}..{:d}')
pr2 = parse.compile('y={:d}, x={:d}..{:d}')

clay = set()
source_loc = (500,0)

spread = [(0, 1), (1, 0), (-1, 0), (0, -1)]

min_y = 1000
max_y = 0

min_x = 500
max_x = 500

for l in ls:
   if l[0] == 'x':
      r = pr.parse(l)
      x = r[0]
      min_y = min(min_y, r[1])
      max_y = max(max_y, r[2])
      min_x = min(min_x, x)
      max_x = max(max_x, x)
      for y in range(r[1], r[2]+1):
         clay.add((x,y))
   else:
      r = pr2.parse(l)
      y = r[0]
      min_y = min(min_y, y)
      max_y = max(max_y, y)
      min_x = min(min_x, r[1])
      max_x = max(max_x, r[2])
      for x in range(r[1], r[2]+1):
         clay.add((x,y))
min_x -= 5
max_x += 5

grid = [[None for _ in range(min_x, max_x+1)] for _ in range(min_y, max_y+3)]

for y,row in enumerate(grid):
   for x,c in enumerate(row):
      if (x+min_x, y+min_y) in clay:
         grid[y][x] = '#'

reached = set()
water = set()

from collections import deque

perc = 0

def run_flow(x,y):
   global perc, min_x, max_x, max_y, grid
   flow_sites = deque([(x,y)])
   while len(flow_sites) > 0:
      x,y = flow_sites.popleft()
      if y >= max_y:
         continue
      min_x = min(x, min_x)
      max_x = max(x, max_x)
      if grid[y][x] != '~':
         grid[y][x] = '|'
      if y+3 >= len(grid):
         continue
      if not grid[y+1][x] in ['#','~'] and (x,y+1) not in flow_sites:
         flow_sites.append((x,y+1))
      else:
         spill_l = spill(x,y,-1)
         spill_r = spill(x,y,1)
         if spill_l[0] and spill_r[0]:
            for i in range(spill_l[1], spill_r[1]+1):
               grid[y][i] = '~'
            if (x, y-1) not in flow_sites:
               flow_sites.append((x,y-1))
         if not spill_l[0] and (spill_l[1], y+1) not in flow_sites:
            flow_sites.append((spill_l[1], y+1))
         if not spill_r[0] and (spill_r[1], y+1) not in flow_sites:
            flow_sites.append((spill_r[1], y+1))


def spill(x,y,dir):
   while grid[y][x+dir] != '#' and grid[y+1][x] in ['#','~']:
      x += dir
      grid[y][x] = '|'
   if grid[y][x+dir] == '#':
      return (True, x)
   else:
      return (False, x)

def print_cs():
   global min_x, min_y, max_x, max_y, clay, water, reached
   with open('log.txt', 'w') as f:
      for y in range(min_y, max_y+1):
         line = ""
         for x in range(min_x, max_x+1):
            if (x,y) in clay:
               line += "#"
            elif (x,y) in water:
               line += "~"
            elif (x,y) in reached:
               line += "|"
            else:
               line += "."
         print(line, file=f)

def sums():
   global grid
   s_r = 0
   s_w = 0
   for row in grid:
      for c in row:
         if c == '~':
            s_r+=1
            s_w+=1
         elif c == '|':
            s_r +=1
   return (s_r, s_w)


run_flow(500-min_x, 0)
sums = sums()
print(f"Part 1: {sums[0]}")
print(f"Part 2: {sums[1]}")
   

      

   
   

   
