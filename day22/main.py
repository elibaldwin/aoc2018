with open('input.txt') as f:
   ls = [s.strip().split() for s in f.readlines()]

depth = int(ls[0][1])
target = [int(a) for a in ls[1][1].split(',')]

width = 150
height = 850

erosion =  [[0 for _ in range(width)] for _ in range(height)]
r_type =  [['' for _ in range(width)] for _ in range(height)]

erosion[0][0] = depth % 20183

for x in range(1,width):
   erosion[0][x] = (x * 16807 + depth) % 20183

for y in range(1,height):
   erosion[y][0] = (y * 48271 + depth) % 20183

for x in range(1,width):
   for y in range(1,height):
      erosion[y][x] = (erosion[y-1][x] * erosion[y][x-1] + depth) % 20183

erosion[target[1]][target[0]] = depth % 20183

types = ['.', '=', '|']

s = 0
for x in range(width):
   for y in range(height):
      t = erosion[y][x] % 3
      if x <= target[0] and y <= target[1]:
         s += t
      r_type[y][x] = types[t]

print(s)

gear_use = {'c':['.', '='], 'n':['=', '|'], 't': ['.', '|']}
gear_opt = {'.':['c', 't'], '=':['c', 'n'], '|': ['n', 't']}

def options(x,y,g_t):
   global r_type
   r_t = r_type[y][x]
   result = []
   for d in [(0,1), (0,-1), (1,0), (-1,0)]:
      ax = x + d[0]
      ay = y + d[1]
      if 0 <= ax < width and 0 <= ay < height and r_t in gear_use[g_t]:
         result.append((ax,ay,g_t,1))
   for nt in gear_opt[r_t]:
      if g_t != nt:
         result.append((x,y,nt,7))
   return result

def m_dist(ax, ay, bx, by):
   return abs(ax - bx) + abs(ay - by)

from collections import deque,defaultdict

def rc_path(came_from,current):
   path = [current]
   while current in came_from:
      path.append(came_from[current])
      current = came_from[current]
   return path

import networkx as nx

def build_nx_digraph(r_type):
   g = nx.DiGraph()
   for y in range(height):
      for x in range(width):
         for tool in ['t','c','n']:
            for op in options(x,y,tool):
               ax,ay,t,cost = op
               g.add_edge((x,y,tool), (ax,ay,t), weight=cost)
   return g


def astar(tx, ty, r_type):
   openq = [(0, 0, 't')]

   closed = set()
   openset = set([(0,0,'t')])

   came_from = {}

   gscore = defaultdict(lambda:100000000)
   gscore[(0,0,'t')] = 0
   fscore = defaultdict(lambda:100000000)
   fscore[(0,0,'t')] = tx+ty

   count = 0

   while len(openq) > 0:
      openq.sort(key=lambda option:fscore[option])
      x,y,tool = openq.pop(0)
      print(x,y,tool)

      if x == tx and y == ty and tool == 't':
         print(gscore[(x,y,tool)])
         print(count)
         return rc_path(came_from, (x,y,tool))
      
      openset.remove((x,y,tool))
      closed.add((x,y,tool))
      count+=1

      for option in options(x,y,tool):
         ax,ay,nt,cost = option

         if (ax,ay,nt) in closed:
            continue
         
         t_gscore = gscore[(x,y,tool)] + cost

         if (ax,ay,nt) not in openset:
            openq.append((ax,ay,nt))
            openset.add((ax,ay,nt))
         elif t_gscore >= gscore[(ax,ay,nt)]:
            continue
         
         came_from[(ax,ay,nt)] = (x,y,tool)
         gscore[(ax,ay,nt)] = t_gscore
         fscore[(ax,ay,nt)] = t_gscore + m_dist(ax,ay,tx,ty) + (7 if nt != 't' else 0)

      
g = build_nx_digraph(r_type)

print(nx.astar_path_length(g, (0,0,'t'), (target[0],target[1],'t')))
