test = True
test = False
if(test):
   fi = 'day7/test.txt'
   workers = 2
   durb = 1
else:
   fi = 'day7/input.txt'
   workers = 6
   durb = 61

with open(fi) as f:
   ls = f.readlines()
from collections import defaultdict
from string import ascii_uppercase

dur = {}

for i, s in enumerate(ascii_uppercase):
   dur[s] = durb + i

children = defaultdict(set)
parents = defaultdict(set)

import parse

dests = set()
starts = set()
for l in ls:
   parser = parse.compile("Step {} must be finished before step {} can begin.")
   r = parser.parse(l)
   children[r[0]].add(r[1])
   parents[r[1]].add(r[0])
   starts.add(r[0])
   dests.add(r[1])


def recurse(items, path):
   items.sort()
   for item in items:
      path.append(item)
      items.remove(item)
      for child in children[item]:
         if parents[child].issubset(set(path)):
            items.append(child)
      if len(items) > 0:
         recurse(items, path)
   return

      
path = []
startitems = list(starts - dests)


recurse(startitems, path)
length = len(path)
print("Part 1: " + ''.join(path))

queue = list(starts - dests)
queue.sort()

def print_info(curr, time):
   info = []
   info.append("Second: " + str(time))
   for c in curr:
      if c != None:
         info.append(c[0])
      else:
         info.append(".")
   info.append(''.join(path))
   print("\t".join(info))

path = []
totalworkers = workers
curr = [None for x in range(workers)]
time = 0
while len(path) < length:
   queue.sort()
   while((None in curr) and len(queue) > 0):
      front = queue.pop(0)
      for i,w in enumerate(curr):
         if w == None:
            curr[i] = [front, dur[front]]
            break
   #print_info(curr, time)
   for i,c in enumerate(curr):
      if c != None:
         c[1]-=1
         if(c[1] == 0):
            curr[i] = None
            path.append(c[0])
            for child in children[c[0]]:
               if parents[child].issubset(set(path)):
                  queue.append(child)
   time += 1
#print_info(curr, time)

print("Part 2: " + str(time))