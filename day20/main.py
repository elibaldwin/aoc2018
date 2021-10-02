with open('input.txt') as f:
   regex = f.read()[1:-1]

from collections import deque
regex = list(regex)
nodecount = 0

class Node:
   def __init__(self):
      global nodecount
      self.edges = []
      self.id = nodecount
      self.loops = False
      nodecount += 1
   
   def max_depth(self, so_far=0):
      if len(self.edges) == 0:
         return so_far
      else:
         if self.loops:
            return self.edges[-1].dest.max_depth(so_far+1)
         else:
            return max([e.dest.max_depth(so_far+1) for e in self.edges])

   def __str__(self):
      if self.loops:
         s = "("
         for i in range(len(self.edges)-1):
            e = self.edges[i]
            s += str(e.dir) + str(e.dest) + "|"
         s += ")"
         return s + str(self.edges[i+1].dir) + str(self.edges[i+1].dest)
      if len(self.edges) == 0:
         return ''
      elif len(self.edges) == 1:
         s = str(self.edges[0].dir)
         if self.edges[0].dest.id < self.id:
            return s
         else:
            return s + str(self.edges[0].dest)
      else:
         s = "(" + str(self.edges[0].dir) + str(self.edges[0].dest)
         for i in range(1,len(self.edges)):
            e = self.edges[i]
            s += "|" + str(e.dir) + str(e.dest)
         return s + ")"


class Edge:
   def __init__(self, direction, n):
      self.dir = direction
      self.dest = n

root = Node()

def build_iter(root, reg):
   queue = deque([(root,reg)])
   while len(queue) > 0:
      rt,re = queue.popleft()
      if len(re) == 0:
         pass
      elif re[0] in ['N','S','E','W']:
         dest = Node()
         edge = Edge(re.pop(0), dest)
         rt.edges.append(edge)
         queue.append((dest,re))
      else:
         lvl = 0
         segs = []
         prev = 1
         for i,c in enumerate(re):
            if c == '(':
               lvl+=1
            elif c == ')':
               lvl-=1
               if lvl < 1:
                  segs.append(re[prev:i])
                  prev = i+1
                  break
            elif c == '|' and lvl == 1:
               segs.append(re[prev:i])
               prev = i+1
         dests = []
         loop = False
         for seg in segs:
            dest = Node()
            if len(seg) > 0:
               edge = Edge(seg.pop(0), dest)
               rt.edges.append(edge)
               dests.append(dest)
            else:
               loop = True
         if loop:
            for i,dest in enumerate(dests):
               seglen = len(segs[i]) // 2
               queue.append((dest, segs[i][:seglen]))
            queue.append((rt, re[prev:]))
         else:
            for i,dest in enumerate(dests):
               queue.append((dest, segs[i]))

def build(root, reg):
   if len(reg) == 0:
      return root
   elif reg[0] in ['N','S','E','W']:
      dest = Node()
      edge = Edge(reg.pop(0), dest)
      root.edges.append(edge)
      return build(dest, reg)
   else: # reg == '('
      lvl = 0
      segs = []
      prev = 1
      for i,c in enumerate(reg):
         if c == '(':
            lvl+=1
         if c == ')':
            lvl-=1
            if lvl < 1:
               segs.append(reg[prev:i])
               prev = i+1
               break
         if c == '|' and lvl == 1:
            segs.append(reg[prev:i])
            prev = i+1
      dests = []
      loop = False
      for seg in segs:
         dest = Node()
         if len(seg) > 0:
            edge = Edge(seg.pop(0), dest)
            root.edges.append(edge)
            dests.append(dest)
         else:
            loop = True
      if loop:
         for i,dest in enumerate(dests):
            fin = build(dest, segs[i])
            fin.edges.append(Edge('', root))
         root.loops = True
         return build(root, reg[prev:])
      else:
         for i,dest in enumerate(dests):
            build(dest, segs[i])

dirs = {'N': (0, -1), 'E':(1, 0), 'S':(0, 1), 'W':(-1,0)}

def depth_above(n,depth):
   queue = deque([(n,0,(0,0))])
   seen = set()
   positions = set()
   while len(queue) > 0:
      node,so_far,pos = queue.popleft()
      seen.add(node.id)
      if so_far >= depth:
         positions.add(pos)
      if len(node.edges) != 0:
         for e in node.edges:
            d = e.dir
            move = dirs[d]
            newpos = (pos[0] + move[0], pos[1] + move[1])
            queue.append((e.dest, so_far+1, newpos))
   return len(positions)

def max_depth(n):
   queue = deque([(n,0)])
   m = 0
   seen = set()
   while len(queue) > 0:
      node,so_far = queue.popleft()
      if node.id in seen:
         continue
      seen.add(node.id)
      if len(node.edges) == 0:
         m = max(m, so_far)
      else:
         for e in node.edges:
            queue.append((e.dest, so_far+1))
   return m

def get_str(n):
   s = ""
   curr = n
   while len(curr.edges) == 1 and curr.id < curr.edges[0].dest.id:
      s += curr.edges[0].dir
      curr = curr.edges[0].dest
   if len(curr.edges) == 0:
      return s
   elif curr.id < curr.edges[0].dest.id:
      if curr.loops:
         s += "("
         for i in range(len(curr.edges)-1):
            s += curr.edges[i].dir + get_str(curr.edges[i].dest) + "|"
         s += ")"
         s += curr.edges[-1].dir + get_str(curr.edges[-1].dest)
      else:
         s += "(" + curr.edges[0].dir + get_str(curr.edges[0].dest)
         for i in range(1,len(curr.edges)):
            e = curr.edges[i]
            s += "|" + e.dir + get_str(e.dest)
         s += ")"
   return s




build_iter(root, regex)

print(f"Part 1: {max_depth(root)}")
#print(f"Part 2: {over1k}")
print(f"Part 2: {depth_above(root,1000)}")