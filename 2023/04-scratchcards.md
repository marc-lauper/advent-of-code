# Day 4 - Scratchcards
See https://adventofcode.com/2023/day/4

## Part 1
```python
import re

sum = 0
with open('aoc4.txt', 'r') as file:
    for line in file:
        sets = re.split(r'\||:', line)
        winning_numbers = re.findall(r'\d+', sets[1])
        scratched_numbers = re.findall(r'\d+', sets[2])
        insersection = list(set(winning_numbers) & set(scratched_numbers))
        if(len(insersection) > 0):
            sum += pow(2, len(insersection) - 1)

print("result:" + str(sum))
```

## Part 2
```python
import re

sum = 0
copies = {}
i = 0

def count_copies(copies, toAdd, index):
    if(index in copies):
        copies[index] += toAdd
    else:
        copies[index] = toAdd

with open('aoc4.txt', 'r') as file:
    for line in file:
        count_copies(copies, 1, i)
        sum += copies[i]

        sets = re.split(r'\||:', line)
        winning_numbers = re.findall(r'\d+', sets[1])
        scratched_numbers = re.findall(r'\d+', sets[2])
        intersection = list(set(winning_numbers) & set(scratched_numbers))
        wins = len(intersection)
        if(wins > 0):
            for j in range(0, wins):
                count_copies(copies, copies[i], i+j+1)
        i+=1

print("result:" + str(sum))
```
