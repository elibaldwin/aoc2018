with open('input.txt') as f:
   ls = f.readlines()

import parse

pr1 = parse.compile('Before: [{}, {}, {}, {}]')
pr2 = parse.compile('After:  [{}, {}, {}, {}]')

ops = []

for i in range(0, len(ls)+1, 4):
   r1 = pr1.parse(ls[i])
   r3 = pr2.parse(ls[i+2])
   r2 = [int(n) for n in ls[i+1].split()]
   l1 = []
   l3 = []
   for j in range(4):
      l1.append(int(r1[j]))
      l3.append(int(r3[j]))
   l2 = tuple(r2)
   ops.append((tuple(l1), l2, tuple(l3)))

def addr(rs, ins):
   out_rs = list(rs)
   out_rs[ins[3]] = rs[ins[1]] + rs[ins[2]]
   return tuple(out_rs)

def addi(rs, ins):
   out_rs = list(rs)
   out_rs[ins[3]] = rs[ins[1]] + ins[2]
   return tuple(out_rs)

def mulr(rs, ins):
   out_rs = list(rs)
   out_rs[ins[3]] = rs[ins[1]] * rs[ins[2]]
   return tuple(out_rs)

def muli(rs, ins):
   out_rs = list(rs)
   out_rs[ins[3]] = rs[ins[1]] * ins[2]
   return tuple(out_rs)

def banr(rs, ins):
   out_rs = list(rs)
   out_rs[ins[3]] = rs[ins[1]] & rs[ins[2]]
   return tuple(out_rs)

def bani(rs, ins):
   out_rs = list(rs)
   out_rs[ins[3]] = rs[ins[1]] & ins[2]
   return tuple(out_rs)

def borr(rs, ins):
   out_rs = list(rs)
   out_rs[ins[3]] = rs[ins[1]] | rs[ins[2]]
   return tuple(out_rs)

def bori(rs, ins):
   out_rs = list(rs)
   out_rs[ins[3]] = rs[ins[1]] | ins[2]
   return tuple(out_rs)

def setr(rs, ins):
   out_rs = list(rs)
   out_rs[ins[3]] = rs[ins[1]]
   return tuple(out_rs)

def seti(rs, ins):
   out_rs = list(rs)
   out_rs[ins[3]] = ins[1]
   return tuple(out_rs)

def gtir(rs, ins):
   out_rs = list(rs)
   out_rs[ins[3]] = 1 if ins[1] > rs[ins[2]] else 0
   return tuple(out_rs)

def gtri(rs, ins):
   out_rs = list(rs)
   out_rs[ins[3]] = 1 if rs[ins[1]] > ins[2] else 0
   return tuple(out_rs)

def gtrr(rs, ins):
   out_rs = list(rs)
   out_rs[ins[3]] = 1 if rs[ins[1]] > rs[ins[2]] else 0
   return tuple(out_rs)

def eqir(rs, ins):
   out_rs = list(rs)
   out_rs[ins[3]] = 1 if ins[1] == rs[ins[2]] else 0
   return tuple(out_rs)

def eqri(rs, ins):
   out_rs = list(rs)
   out_rs[ins[3]] = 1 if rs[ins[1]] == ins[2] else 0
   return tuple(out_rs)

def eqrr(rs, ins):
   out_rs = list(rs)
   out_rs[ins[3]] = 1 if rs[ins[1]] == rs[ins[2]] else 0
   return tuple(out_rs)

opfns = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]

def match(fn, rs, ins, out):
   return fn(rs, ins) == out

def num_matches(rs, ins, out):
   global opfns
   s = 0
   for op in opfns:
      if match(op, rs, ins, out):
         s += 1
   return s

def matches(rs, ins, out):
   global opfns
   ms = set()
   for i, op in enumerate(opfns):
      if match(op, rs, ins, out):
         ms.add(i)
   return ms

from collections import defaultdict


#total = sum([1 for op in ops if num_matches(op[0], op[1], op[2]) >= 3])
   
#print(total)
#print(ops[0])

examples = defaultdict(list)
mmap = {}

for op in ops:
   opcode = op[1][0]
   examples[opcode].append(op)

for k,v in examples.items():
   rs,ins,out = v[0]
   mmap[k] = matches(rs,ins,out)

while(sum([len(mmap[i]) for i in range(16)]) > 16):
   for i in range(16):
      if len(mmap[i]) == 1:
         for j in range(16):
            if i != j:
               mmap[j] -= mmap[i]

opmap = {}

for i in range(16):
   opmap[i] = list(mmap[i])[0]

print(opmap)

with open('input2.txt') as f:
   program = [tuple([int(s) for s in l.split()]) for l in f.readlines()]

reg = (0,0,0,0)

for op in program:
   reg = opfns[opmap[op[0]]](reg, op)

print(reg)







