# Day 11 - Cosmic Expansion
See https://adventofcode.com/2023/day/11

```python
EXPANSION_RATE = 1000000 # 1 for part 1, 1000000 for part 2

class Galaxy:
    def __init__(self):
        self.x = 0
        self.y = 0

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __repr__(self):
        return str(self)

galaxies = []
with open('aoc11.txt', 'r') as file:
    x = 0
    for line in file:
        line_cells = list(line)
        for y in range(len(line_cells)):
            if(line_cells[y] == '#'):
                galaxy = Galaxy()
                galaxy.x = x
                galaxy.y = y
                galaxies.append(galaxy)
        x += 1

if EXPANSION_RATE > 1:
    EXPANSION_RATE -= 1

# EXPAND GALAXIES ON X-AXIS
############################
galaxies.sort(key=lambda x: x.x)
original_size = len(galaxies)
previous_x = 0
for x in reversed(range(original_size)):
    diff = previous_x - galaxies[x].x
    previous_x = galaxies[x].x
    if(diff > 1):
        for i in range(x+1, original_size):
            galaxies[i].x += (diff - 1) * EXPANSION_RATE

# EXPAND GALAXIES ON Y-AXIS
############################
galaxies.sort(key=lambda x: x.y)
original_size = len(galaxies)
previous_y = 0
for y in reversed(range(original_size)):
    diff = previous_y - galaxies[y].y
    previous_y = galaxies[y].y
    if(diff > 1):
        for i in range(y+1, original_size):
            galaxies[i].y += (diff - 1) * EXPANSION_RATE

sum = 0
for index1 in range(len(galaxies)-1):
    for index2 in range(index1+1, len(galaxies)):
        sum += abs(galaxies[index1].x - galaxies[index2].x) + abs(galaxies[index1].y - galaxies[index2].y)

print("result:" + str(sum))
```