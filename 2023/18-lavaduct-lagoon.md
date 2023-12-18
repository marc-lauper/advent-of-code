
# Day 18 - Lavaduct Lagoon
See https://adventofcode.com/2023/day/18

## Part 1
```python
import string

VERBOSE = False
class Vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return str(self)

def print_verbose(text):
    if VERBOSE:
        print(text)

def computeArea(vertices):
    result = 0
    for i in range(len(vertices)):
        j = (i + 1) % len(vertices)
        result += vertices[i].x * vertices[j].y
        result -= vertices[j].x * vertices[i].y
    result = abs(result) / 2
    return result

vertices = []
total_distance = 0
with open('aoc18.txt', 'r') as file:
    x = 0
    y = 0
    vertex = Vertex(x, y)
    vertices.append(vertex)
    for line in file:
        line = line.replace('\n', '')
        if(len(line) == 0):
            continue

        tokens = line.split(' ')
        direction= tokens[0]
        distance = int(tokens[1])
        color = tokens[2] # We don't care about it, for now
        print_verbose(f"Direction: {direction}, Distance: {distance}, Color: {color}")
        
        if(direction == 'R'):
            x += distance
        elif(direction == 'L'):
            x -= distance
        elif(direction == 'U'):
            y -= distance
        elif(direction == 'D'):
            y += distance
        
        total_distance += distance
        
        vertex = Vertex(x, y)
        vertices.append(vertex)

for vertex in vertices:
    print(vertex)

# See https://en.wikipedia.org/wiki/Pick%27s_theorem
result = computeArea(vertices) + total_distance / 2 + 1
print(f"result: {result}")
```