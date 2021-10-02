
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
            if c % 100 == 0:
               print(c)
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

print(sim(0))