with open('input.txt') as f:
   g = [list(s.strip()) for s in f.readlines()]

lenx = len(g[0])
leny = len(g)
adj = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
# order: empty, tree, lumber
types = ['.', '|', '#']

def next_type(x,y):
   global g
   totals = [0,0,0]
   for dy,dx in adj:
      ay = y + dy
      ax = x + dx
      if ax in range(0, lenx) and ay in range(0, leny):
         for i,c in enumerate(types):
            if g[ay][ax] == c:
               totals[i] += 1
               break
   if g[y][x] == '.':
      return '|' if totals[1] >= 3 else '.'
   if g[y][x] == '|':
      return '#' if totals[2] >= 3 else '|'
   return '#' if totals[1] >= 1 and totals[2] >= 1 else '.'

def get_value(g):
   totals = [0,0,0]
   for row in g:
      for c in row:
         for i,t in enumerate(types):
            if c == t:
               totals[i]+=1
               break
   return totals[1]*totals[2]

sequence = []
for i in range(700):
   next_g = [[next_type(x,y) for x,_ in enumerate(row)] for y,row in enumerate(g)]
   g = next_g
   val = get_value(g)
   if val in sequence:
      print(i,sequence.index(val))
   sequence.append(val)

print(sequence[600:628])
print(sequence[628:656])
print(sequence[599 + (1000000000 - 600) % 28])




