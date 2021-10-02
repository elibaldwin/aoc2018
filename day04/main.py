import parse
import datetime

#[1518-10-03 00:47] falls asleep
#[1518-07-26 23:50] Guard #487 begins shift
#[1518-06-22 00:48] wakes up

with open('day4/input.txt') as f:
    ls = f.readlines()

events = {}
sequence = []

parser = parse.compile("[{year:d}-{month:d}-{day:d} {hr:d}:{min:d}] {}")
for l in ls:
    r = parser.parse(l)
    time = datetime.datetime(r['year'], r['month'], r['day'], r['hr'], r['min'])
    events[time] = r[0]
    sequence.append(time)

sequence.sort()

parser = parse.compile("Guard #{:d} begins shift")
curr_id = 0
prev_t = 0
counts = {}
for t in sequence:
    s = events[t]
    if "Guard" in s:
        curr_id = parser.parse(s)[0]
        if curr_id not in counts:
            counts[curr_id] = [[0 for x in range(60)], 0]
    if "falls" in s:
        prev_t = t.minute
    if "wakes" in s:
        while prev_t < t.minute:
            counts[curr_id][0][prev_t] += 1
            counts[curr_id][1] += 1
            prev_t += 1

maxn = 0
best = None
for k,v in counts.items():
    if v[1] > maxn:
        best = k
        maxn = v[1]

bestm = counts[best][0].index(max(counts[best][0]))

print("Part 1: " + str((bestm * best)))

minute = 0
best = None
maxn = 0
for k,v in counts.items():
    maxc = max(v[0])
    if maxc > maxn:
        best = k
        minute = v[0].index(maxc)
        maxn = maxc

print("Part 2: " + str(minute * best))

