# Day 2 - Cube Conondrum
See https://adventofcode.com/2023/day/2

```python
import re;

limit_red = 12
limit_green = 13
limit_blue = 14

def find_max(pattern, line):
    matches = re.findall(pattern, line)
    if matches:
        result = max(list(map(int, matches)))
    else:
        result = 0
    return int(result)

sum1 = 0
sum2 = 0
with open('aoc2.txt', 'r') as file:
    for line in file:

        game = re.findall(r'Game (\d+)', line)[0]
        red = find_max(r'(\d+) red', line)
        green = find_max(r'(\d+) green', line)
        blue = find_max(r'(\d+) blue', line)
        
        if(red <= limit_red and green <= limit_green and blue <= limit_blue):
            sum1 += int(game)

        power = red * green * blue
        sum2 += power
    
    print("result1:" + str(sum1))
    print("result2:" + str(sum2))
```