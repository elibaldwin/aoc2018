with open('input.txt') as f:
   code = [s.strip().split() for s in f.readlines()]

for i in range(len(code)):
   for j in range(1,len(code[i])):
      code[i][j] = int(code[i][j])

code = [tuple(l) for l in code]
def addr(rs, ins):
   rs[ins[3]] = rs[ins[1]] + rs[ins[2]]

def addi(rs, ins):
   rs[ins[3]] = rs[ins[1]] + ins[2]

def mulr(rs, ins):
   rs[ins[3]] = rs[ins[1]] * rs[ins[2]]

def muli(rs, ins):
   rs[ins[3]] = rs[ins[1]] * ins[2]

def banr(rs, ins):
   rs[ins[3]] = rs[ins[1]] & rs[ins[2]]

def bani(rs, ins):
   rs[ins[3]] = rs[ins[1]] & ins[2]

def borr(rs, ins):
   rs[ins[3]] = rs[ins[1]] | rs[ins[2]]

def bori(rs, ins):
   rs[ins[3]] = rs[ins[1]] | ins[2]

def setr(rs, ins):
   rs[ins[3]] = rs[ins[1]]

def seti(rs, ins):
   rs[ins[3]] = ins[1]

def gtir(rs, ins):
   rs[ins[3]] = 1 if ins[1] > rs[ins[2]] else 0

def gtri(rs, ins):
   rs[ins[3]] = 1 if rs[ins[1]] > ins[2] else 0

def gtrr(rs, ins):
   rs[ins[3]] = 1 if rs[ins[1]] > rs[ins[2]] else 0

def eqir(rs, ins):
   rs[ins[3]] = 1 if ins[1] == rs[ins[2]] else 0

def eqri(rs, ins):
   rs[ins[3]] = 1 if rs[ins[1]] == ins[2] else 0

def eqrr(rs, ins):
   rs[ins[3]] = 1 if rs[ins[1]] == rs[ins[2]] else 0

opfns = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]
fnstrs= ['addr', 'addi', 'mulr', 'muli', 'banr', 'bani', 'borr', 'bori', 'setr', 'seti', 'gtir', 'gtri', 'gtrr', 'eqir', 'eqri', 'eqrr']

fnmap = {}
for i in range(len(opfns)):
   fnmap[fnstrs[i]] = opfns[i]


init_ip = code[0][1]
code = code[1:]

registers = [0,0,0,0,0,0]

ip = registers[init_ip]
for i in range(10):
   registers[init_ip] = ip
   optype = code[ip][0]
   fnmap[optype](registers, code[ip])
   ip = registers[init_ip]
   ip +=1

import math

num = max(registers)
factors = []

for i in range(1, round(math.sqrt(num))+1):
   if num % i == 0:
      factors.append(i)
      factors.append(num // i)

print(f"Part 1: {sum(factors)}")

registers = [1,0,0,0,0,0]

ip = registers[init_ip]
for i in range(20):
   registers[init_ip] = ip
   optype = code[ip][0]
   fnmap[optype](registers, code[ip])
   ip = registers[init_ip]
   ip +=1

num = max(registers)
factors = []

for i in range(1, round(math.sqrt(num))+1):
   if num % i == 0:
      factors.append(i)
      factors.append(num // i)

print(f"Part 2: {sum(factors)}")