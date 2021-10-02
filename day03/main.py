with open('day3/input.txt') as f:
    ls = f.readlines()

import re
g = [[[0,None] for x in range(1000)] for y in range(1000)]

lls = {}
for l in ls:
    l = re.sub('[#:]', '', l)
    ll = l.split(' ')
    coords = ll[2].split(',')
    r = ll[3].split('x')
    r = (int(r[0]), int(r[1]))
    coords = (int(coords[0]), int(coords[1]))
    for x in range(coords[0], coords[0]+r[0]):
        for y in range(coords[1], coords[1]+r[1]):
            g[x][y][0] += 1
            g[x][y][1] = ll[0]
    lls[ll[0]] = (coords, r)
    

possible = set()
result = 0
for x in g:
    for y in x:
        if y[0] >= 2:
            result += 1
        if y[0] == 1:
            possible.add(y[1])

print("Part 1: " + str(result))

for option in possible:
    coords = lls[option][0]
    r = lls[option][1]
    allone = True
    for x in range(coords[0], coords[0]+r[0]):
        for y in range(coords[1], coords[1]+r[1]):
            if g[x][y][0] != 1:
                allone = False
    if allone:
        result = option

print("Part 2: " + str(result))