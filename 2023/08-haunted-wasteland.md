# Day 8 - Haunted Wasteland
See https://adventofcode.com/2023/day/8

## Part 1
```python
import re

nodes = {}

path = ""
with open('aoc8.txt', 'r') as file:
    first = True
    for line in file:
        line = line.replace('\n', '')
        if(first):
            path = line
            first = False
            continue
        
        parsed = re.findall(r'[A-Z]{3}', line)
        if(len(parsed) == 3):
            key = parsed[0]
            left = parsed[1]
            right = parsed[2]
            if(key != left or key != right):
                nodes[key] = {}
                nodes[key]['L'] = left
                nodes[key]['R'] = right

result = 0
START = "AAA"
END = "ZZZ"
currentNode = START
pathPosition = 0
pathLength = len(path)
while currentNode != END:
    result+=1
    key = path[pathPosition]
    currentNode = nodes[currentNode][key]
    if(currentNode == None):
        print("Error: " + key + " not found")
        break
    pathPosition+=1
    if(pathPosition == pathLength):
        pathPosition = 0

print("result:" + str(result))
```
## Part 2
```python
import re, math, itertools

nodes = {}
currentNodes = []

path = ""
with open('aoc8.txt', 'r') as file:
    first = True
    for line in file:
        line = line.replace('\n', '')
        if(first):
            path = line
            first = False
            continue
        
        parsed = re.findall(r'[\w]{3}', line)
        if(len(parsed) == 3):
            key = parsed[0]
            left = parsed[1]
            right = parsed[2]
            nodes[key] = {}
            nodes[key]['L'] = left
            nodes[key]['R'] = right
            if key[-1] == 'A':
                currentNodes.append(key)

print ("Current nodes: " + str(currentNodes))
ends = []
for currentNode in currentNodes:
    print("NEXT PATH STARTING FROM: " + currentNode)
    for steps, key in enumerate(itertools.cycle(path)):
        currentNode = nodes[currentNode][key]
        if currentNode[-1] == 'Z':
            print("FOUND END: " + currentNode + " at position " + str(key))
            break
    ends.append(steps + 1)
print(math.lcm(*ends))

# print("result:" + str(result))
```