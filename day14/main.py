input = 440231
#input = 18
input2 = [4,4,0,2,3,1]

from collections import deque

recipes = [3,7]
e1 = 0
e2 = 1
while(True):
   new_recipe = recipes[e1] + recipes[e2]
   if(new_recipe > 9):
      recipes.append(new_recipe // 10)
   if(recipes[-6:] == input2):
      print(recipes[-6:])
      break
   recipes.append(new_recipe % 10)
   if(recipes[-6:] == input2):
      print(recipes[-6:])
      break
   e1 += recipes[e1] + 1
   e2 += recipes[e2] + 1
   e1 %= len(recipes)
   e2 %= len(recipes)


print(len(recipes) - 6)
print(recipes[input:input+10])
