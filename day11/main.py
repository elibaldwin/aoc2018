from collections import defaultdict

def add_sums(g,x,y,pls):
   max_size = min(300-x, 300-y, 30)
   pl_sum = 0
   for s in range(1, max_size+1):
      for i in range(s):
         pl_sum += g[x+i][y+s-1]
      for i in range(s-1):
         pl_sum += g[x+s-1][y+i]
      pls[(x,y,s)] = pl_sum

def sum_sqr(g,x,y,s):
   sum = 0
   for i in range(x, x+s):
      for j in range(y, y+s):
         sum += g[i][j]
   return sum

def get_grid(serial):
   g = [[0 for _ in range(301)] for _ in range(301)]
   for x in range(1,301):
      for y in range(1,301):
         rid = x + 10
         pl = rid * y
         pl += serial
         pl *= rid
         pl = (pl // 100) % 10
         pl -= 5
         g[x][y] = pl
   return g

def get_best(g):
   pls = {}
   for i in range(1,300):
      for j in range(1,300):
         add_sums(g,i,j,pls)
   maxv = 0
   best = ()
   for k,v in pls.items():
      if v > maxv:
         maxv = v
         best = k
   return best

g = get_grid(5235)

print("Part 2: " + str(get_best(g)))