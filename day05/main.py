with open('day5/input.txt') as f:
   i = f.read()

import string

matches = [(x + x.upper()) for x in string.ascii_lowercase] + [(x.upper() + x) for x in string.ascii_lowercase]

def p1(arg):
   prev_len = len(arg) + 1
   while(len(arg) < prev_len):
      prev_len = len(arg)
      for m in matches:
         arg = arg.replace(m, "")
   return arg

first = p1(i)
result = len(first)

print("Part 1: " + str(result))

result = len(i)
for char in string.ascii_lowercase:
   temp = first.replace(char, "").replace(char.upper(), "")
   result = min(result, len(p1(temp)))

print("Part 2: " + str(result))