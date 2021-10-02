with open('input.txt') as f:
   ls = [list(l.replace('\n', '')) for l in f.readlines()]

dirs = ['^', '<', 'v', '>']
moves = [(-1, 0), (0, -1), (1, 0), (0, 1)]
turns = [1, 0, 3]

carts = []

for i,row in enumerate(ls):
   for j,c in enumerate(row):
      if c in dirs:
         carts.append([i,j,dirs.index(c),0])
      if c == '>' or c == '<':
         ls[i][j] = "-"
      if c == '^' or c =='v':
         ls[i][j] = "|"

carts.sort()
crashed = []

def move(cart, dir, carts):
   global crashed
   move = moves[dir]
   cart[0] += move[0]
   cart[1] += move[1]
   for c in carts:
      if c != cart:
         if c[:2] == cart[:2]:
            crashed.append(c)
            crashed.append(cart)

def increment(carts, ls):
   global crashed
   carts.sort()
   for c in carts:
      track = ls[c[0]][c[1]]
      if track == '/':
         if c[2] == 0 or c[2] == 2:
            c[2] = (c[2] + 3) % 4
         else:
            c[2] = (c[2] + 1) % 4
      elif track == '\\':
         if c[2] == 0 or c[2] == 2:
            c[2] = (c[2] + 1) % 4
         else:
            c[2] = (c[2] + 3) % 4
      elif track == '+':
         c[2] = (c[2] + turns[c[3]]) % 4
         c[3] = (c[3] + 1) % 3
      move(c, c[2], carts)
   for c in crashed:
      carts.remove(c)
   crashed = []
         

def print_map(ls, carts):
   co = [row[:] for row in ls]
   for c in carts:
      if(c[1] >= len(co[0])): print(c)
      co[c[0]][c[1]] = dirs[c[2]]
   for r in co:
      print(''.join(r))
   print()

while(len(carts) > 1):
   #print_map(ls, carts)
   increment(carts, ls)
   #check_collisions(carts)
   

print(carts)





