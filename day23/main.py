with open('input.txt') as f:
   ls = [s.strip() for s in f.readlines()]

import parse

pr = parse.compile('pos=<{:d},{:d},{:d}>, r={:d}')

particles = []

c = 0
for l in ls:
   r = pr.parse(l)
   particles.append((r[0],r[1],r[2],r[3],c))
   c+=1

m = 0
best = None

for p in particles:
   if p[3] > m:
      m = p[3]
      best = p
   
def m_dist(a, b):
   return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])

s = 0
for p in particles:
   d = m_dist(best,p)
   if d <= best[3]:
      s+=1

print("Part 1: {}".format(s))

def overlaps(a, b):
   return a[3] + b[3] >= m_dist(a,b)

def overlap_q(a, b):
   return a[3] + b[3] - m_dist(a,b)

def in_range(a, b): #true if point a is in range of nanobot b
   return m_dist(a,b) <= b[3]


overlapping = set()

for a in particles:
   for b in particles:
      if overlaps(a,b):
         overlapping.add((a[4], b[4]))

print("found overlapping pairs")

overlapsets = []
for a in particles:
   os = set([a])
   for b in particles:
      if (a[4],b[4]) in overlapping:
         os.add(b)
   overlapsets.append(os)

print("finished with overlapping sets")

def reduce_overlap(group):
   to_remove = set()
   for a in group:
      for b in group:
         if (a[4],b[4]) not in overlapping:
            to_remove.add(a)
            break
   return group - to_remove

m = 0
best = None
reduced_sets = []
for i,g in enumerate(overlapsets):
   newg = reduce_overlap(g)
   reduced_sets.append(newg)
   if len(newg) > m:
      m = len(newg)
      best = newg
   if (i+1) % 10 == 0:
      print("{} of {} completed".format(i+1,1000))

print("finished reducing sets")

with open('best.txt', 'w') as f:
   for p in best:
      f.write(' '.join([str(i) for i in p]) + '\n')





      







