with open('input.txt') as f:
   g = [list(s.strip()) for s in f.readlines()]


characters_og = []
safe_cells_og = set()
g_cells_og = set()
e_cells_og = set()

characters = []
safe_cells = set()
g_cells = set()
e_cells = set()

elf_dmg = 3

for x,row in enumerate(g):
   for y,c in enumerate(row):
      if c == '.':
         safe_cells_og.add((x,y))
      if c in ['G','E']:
         characters_og.append([x,y,c,200])
         g[x][y] = '.'

for char in characters_og:
   if char[2] == 'E':
      e_cells_og.add(tuple(char[:2]))
   if char[2] == 'G':
      g_cells_og.add(tuple(char[:2]))
   
def reset():
   global characters, characters_og, safe_cells, safe_cells_og, g_cells, g_cells_og, e_cells, e_cells_og
   characters = [c.copy() for c in characters_og]
   safe_cells = safe_cells_og.copy()
   g_cells = g_cells_og.copy()
   e_cells = e_cells_og.copy()

reset()

adj = [(-1,0), (0, -1), (0, 1), (1, 0)]

def adj_cells(l):
   return [(l[0] + a[0], l[1] + a[1]) for a in adj]

def valid_adj_cells(l, t):
   global safe_cells, e_cells, g_cells
   if(t == 'G'):
      return [c for c in adj_cells(l) if c in (safe_cells | e_cells)]
   else:
      return [c for c in adj_cells(l) if c in (safe_cells | g_cells)]

def has_target(char):
   global characters
   enemies = [a for a in characters if a[2] != char[2]]
   return len(enemies) > 0


def get_adj_target(char):
   global characters
   adj = adj_cells(char[:2])
   min_hp = 201
   best = None
   enemies = [a for a in characters if a[2] != char[2]]
   for o in enemies:
      if tuple(o[:2]) in adj:
         if o[3] < min_hp:
            best = o
            min_hp = o[3]
   return best


def search(char):
   global e_cells, g_cells
   target_set = e_cells if (char[2] == 'G') else g_cells
   root = (0, char[0], char[1])

   queue = [root]
   paths = {}
   paths[root] = []
   visited = set()

   while len(queue) > 0:
      #queue.sort()
      subroot = queue.pop(0)
      dist = subroot[0]

      for cell in adj_cells(subroot[1:]):
         if cell in target_set:
            return paths[subroot]
      
      nextcells = valid_adj_cells(subroot[1:], char[2])
      nextcells.sort()

      for cell in nextcells:
         if cell in visited:
            continue
         subpath = paths[subroot].copy()
         subpath.append(cell)
         paths[(dist+1, cell[0], cell[1])] = subpath
         queue.append((dist+1, cell[0], cell[1]))
         visited.add(cell)
   return None

def move_char(char, loc):
   global g_cells, e_cells, safe_cells
   type_set = e_cells if (char[2] == 'E') else g_cells
   type_set.remove(tuple(char[:2]))
   safe_cells.add(tuple(char[:2]))
   char[0] = loc[0]
   char[1] = loc[1]
   type_set.add(loc)
   safe_cells.remove(loc)

def attack_char(char):
   global g_cells, e_cells, safe_cells, characters, elf_dmg
   type_set = e_cells if (char[2] == 'E') else g_cells
   char[3] -= (3 if char[2] == 'E' else elf_dmg)
   if char[3] <= 0:
      charloc = tuple(char[:2])
      type_set.remove(charloc)
      safe_cells.add(charloc)
      return True
   return False


def print_grid(g, i):
   characters.sort()
   global g_cells, e_cells
   with open('log.txt', 'a') as f:
      print(f"After round {i+1}:", file=f)
      for x, row in enumerate(g):
         s = []
         for y,c in enumerate(row):
            if((x,y) in g_cells):
               s.append('G')
            elif ((x,y) in e_cells):
               s.append('E')
            else:
               s.append(c)
         print(''.join(s) + " " + ", ".join([str([c[2], c[3]]) for c in characters if c[0] == x]), file=f)
      print(file=f)

def sim_rounds(n):
   global g_cells, e_cells, characters
   print_grid(g, -1)

   for i in range(n):
      characters.sort()
      ind = 0
      while ind < len(characters):
         char = characters[ind]
         if not has_target(char):
            #print_grid(g)
            return i
         target = get_adj_target(char)
         if target == None:
            path = search(char)
            if path != None and len(path) > 0:
               move_char(char, path[0])
               target = get_adj_target(char)
         if target != None:
            if target[3] > 0:
               if attack_char(target):
                  if characters.index(target) < ind:
                     ind -=1
                  characters.remove(target)
         ind+=1
      characters = [c for c in characters if c[3] > 0]
      print_grid(g,i)
      #print(f"{len(g_cells)} Goblins remaining, {len(e_cells)} Elves remaining after round {i+1}.")
   return -1

def outcome(rounds, characters):
   return rounds * sum([c[3] for c in characters])


for i in range(4,50):
   reset()
   elf_dmg = i
   rounds = sim_rounds(200)
   print(f"{len(e_cells)} elves are still alive")
   if len(e_cells_og) == len(e_cells):
      print(outcome(rounds, characters))
      break
   else:
      print(f"{i} is not enough.")


