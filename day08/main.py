with open ('day8/input.txt') as f:
   ns = [int(x) for x in f.read().split()]

from collections import defaultdict

tree = defaultdict(list)
vals = defaultdict(list)
count = 0

def build(ns, tree):
   global count
   count += 1
   nchld = ns.pop(0)
   nmeta = ns.pop(0)
   num = count
   for _ in range(nchld):
      tree[num].append(build(ns, tree))
   for _ in range(nmeta):
      vals[num].append(ns.pop(0))
   return num

build(ns, tree)

metatotal = 0
for v in vals.values():
   metatotal += sum(v)

print("Part 1: " + str(metatotal))

def val(n):
   children = tree[n]
   if len(children) > 0:
      count = 0
      meta = vals[n]
      for v in meta:
         if v-1 < len(children):
            count += val(children[v-1])
      return count
   else:
      return sum(vals[n])

print("Part 2: " + str(val(1)))