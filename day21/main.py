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
codelen = len(code)
c = 0

registers = [0,0,0,0,0,0]

ip = registers[init_ip]
haltvals = set()
while ip < codelen:
   registers[init_ip] = ip
   optype = code[ip][0]
   fnmap[optype](registers, code[ip])
   ip = registers[init_ip]
   ip +=1
   c+=1
   if ip == 28:
      print("Part 1: {}".format(registers[4]))
      break

def sim(start):
   r = [start,0,0,0,0,0]
   haltvals = set()
   c = 0
   prevval = 0
   while True:
      r[5] = r[4] | 65536
      r[4] = 1765573
      while True:
         r[1] = r[5] & 255
         r[4] += r[1]
         r[4] = r[4] & 16777215
         r[4] *= 65899
         r[4] = r[4] & 16777215
         if r[5] < 256:
            if r[4] in haltvals:
               return prevval
            else:
               haltvals.add(r[4])
               prevval = r[4]
               c+=1
            if r[4] == r[0]:
               return
            else:
               break
         r[1] = 0
         while True:
            r[3] = r[1] + 1
            r[3] *= 256
            if r[3] > r[5]:
               break
            r[1] += 1
         r[5] = r[1]

print("Part 2: {}".format(sim(0)))

