with open('input.txt') as f:
   ls = [s.strip() for s in f.readlines()]

import parse
from z3 import *

pr = parse.compile('pos=<{:d},{:d},{:d}>, r={:d}')

bots = []

for l in ls:
   r = pr.parse(l)
   bots.append((r[0],r[1],r[2],r[3]))

def z3abs(x):
   return If(x >= 0,x,-x)

def z3mdist(a,b):
   return z3abs(a[0]-b[0]) + z3abs(a[1]-b[1]) + z3abs(a[2]-b[2])

x = Int('x')
y = Int('y')
z = Int('z')

origin = (x,y,z)
c_expr = x * 0
for ax,ay,az,r in bots:
   c_expr += If(z3mdist(origin, (ax,ay,az)) <= r, 1, 0)

o = Optimize()
print("start optimize")
o.maximize(c_expr)
o.minimize(z3mdist((0,0,0), origin))

print(o.check())
print(o.model())