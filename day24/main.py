with open('input.txt') as f:
   ls = [h.split('\n')[1:] for h in f.read().split('\n\n')]

import parse

pr1 = parse.compile('{num:d} units each with {hp:d} hit points{special}with an attack that does {dp:d} {dp_type} damage at initiative {init:d}')

class Group:
   def __init__(self, num, hp, dp, dp_type, init, weaknesses=[], immunities=[]):
      self.num = num
      self.hp = hp
      self.dp = dp
      self.dp_type = dp_type
      self.init = init
      self.weaknesses = set(weaknesses)
      self.immunities = set(immunities)
      self.boost = 0
   
   def eff_pw(self):
      return self.num * (self.dp + self.boost)
   
   def damage_from(self, other):
      t = other.dp_type
      if t in self.immunities:
         return 0
      elif t in self.weaknesses:
         return other.eff_pw() * 2
      else:
         return other.eff_pw()
      
   def attack(self, dmg):
      n = dmg // self.hp
      self.num -= n
      return self.num > 0
   
   def set_boost(self, boost):
      self.boost = boost

   def __lt__(self, other):
      return (self.eff_pw(), self.init) > (other.eff_pw(), other.init)
   
   def __eq__(self, other):
      return self.init == other.init

   def __str__(self):
      return f"has {self.num} units who deal {self.dp} {self.dp_type} damage, have {self.hp} health and are weak to {str(self.weaknesses)} and immune to {str(self.immunities)}"

   
def parse_armies():
   global ls
   immune = []
   infection = []

   sppr = parse.compile('{} to {}')

   for l in ls[0]:
      r = pr1.parse(l)
      sp = r['special']
      if len(sp) > 1:
         sp = sp.strip().replace('(', '').replace(')', '')
         sp = sp.split('; ')
         weaknesses = []
         immunities = []
         for s in sp:
            spr = sppr.parse(s)
            if spr[0] == 'weak':
               weaknesses = spr[1].split(', ')
            else:
               immunities = spr[1].split(', ')
         u = Group(r['num'], r['hp'], r['dp'], r['dp_type'], r['init'], weaknesses, immunities)
      else:
         u = Group(r['num'], r['hp'], r['dp'], r['dp_type'], r['init'])
      immune.append(u)

   for l in ls[1]:
      r = pr1.parse(l)
      sp = r['special']
      if len(sp) > 1:
         sp = sp.strip().replace('(', '').replace(')', '')
         sp = sp.split('; ')
         weaknesses = []
         immunities = []
         for s in sp:
            spr = sppr.parse(s)
            if spr[0] == 'weak':
               weaknesses = spr[1].split(', ')
            else:
               immunities = spr[1].split(', ')
         u = Group(r['num'], r['hp'], r['dp'], r['dp_type'], r['init'], weaknesses, immunities)
      else:
         u = Group(r['num'], r['hp'], r['dp'], r['dp_type'], r['init'])
      infection.append(u)
   return (immune, infection)

def battle(army1, army2):
   rd = 1
   while len(army1) > 0 and len(army2) > 0:

      q1 = sorted(army1)
      q2 = sorted(army2)

      pairs = []
      
      for i,g in enumerate(q1):
         m = 0
         target = None
         for j, t in enumerate(q2):
            dmg = t.damage_from(g)
            if dmg > m:
               m = dmg
               target = t
         if m > 0:
            pairs.append((g,target))
            q2.remove(target)
      q2 = sorted(army2)
      for g in q2:
         m = 0
         target = None
         for j, t in enumerate(q1):
            dmg = t.damage_from(g)
            if dmg > m:
               m = dmg
               target = t
         if m > 0:
            pairs.append((g,target))
            q1.remove(target)
      
      pairs.sort(key=lambda pair: pair[0].init, reverse=True)

      dead = []
      for atk,dfn in pairs:
         if atk not in dead:
            dmg = dfn.damage_from(atk)
            if not dfn.attack(dmg):
               dead.append(dfn)
      
      for d in dead:
         if d in army1:
            army1.remove(d)
         if d in army2:
            army2.remove(d)
      rd += 1
   if len(army1)>0:
      
      return sum([g.num for g in army1])
   elif len(army2)>0:
      return sum([g.num for g in army2])

immune, infection = parse_armies()

boost = 30
for g in immune:
   g.set_boost(boost)
print(battle(infection, immune))
print("immune system won!" if len(immune)>0 else "lost :(")


