with open('best.txt') as f:
   bots = [[int(s) for s in l.strip().split()] for l in f.readlines()]

def m_dist(a, b):
   return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])

def in_range(a, b): #true if point a is in range of nanobot b
   return m_dist(a,b) <= b[3]

avgs = [0,0,0]
for i in range(3):
   avgs[i] = sum([b[i] for b in bots]) / len(bots)

bots1d = []

mind = 1000000000000000
maxd = 0
minmax = 100000000000000000
maxmin = 0
for b in bots:
   mindist = m_dist((0,0,0), b) - b[3]
   maxdist = m_dist((0,0,0), b) + b[3]
   mind = min(mind, mindist)
   maxd = max(maxd, maxdist)
   minmax = min(minmax, maxdist)
   maxmin = max(maxmin, mindist)
   bots1d.append((mindist, maxdist, b[4]))

print(f"Part 2: {maxmin}")





