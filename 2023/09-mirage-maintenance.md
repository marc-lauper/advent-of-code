# Day 9 - Mirage Maintenance
See https://adventofcode.com/2023/day/9

```python
import re

class Sequence:
    def __init__(self):
        self.steps = []
        self.part1 = 0
        self.part2 = 0

sequences = []

with open('aoc9.txt', 'r') as file:
    for line in file:
        seq = Sequence()
        seq.steps.append(list(map(int, line.split(' '))))
        sequences.append(seq)

for sequence in sequences:
    print("NEW SEQUENCE:")
    all_zeroes = False
    step = 0
    while(not all_zeroes):
        all_zeroes = True
        diffs = []
        print("step " + str(step) + ": " + str(sequence.steps[step]))
        for i in range(0, len(sequence.steps[step]) - 1):
            diff = sequence.steps[step][i + 1] - sequence.steps[step][i]
            diffs.append(diff)
            all_zeroes = all_zeroes and diff == 0
        sequence.steps.append(diffs)
        step += 1

    for i in range (len(sequence.steps) - 1, 0, -1):
        sequence.steps[i-1].append(sequence.steps[i-1][-1] + sequence.steps[i][-1])
        sequence.steps[i-1].insert(0, sequence.steps[i-1][0] - sequence.steps[i][0])
    sequence.part1 = sequence.steps[0][-1]
    sequence.part2 = sequence.steps[0][0]

result1 = 0
result2 = 0
for sequence in sequences:
    result1 += sequence.part1
    result2 += sequence.part2

print("result part 1:" + str(result1))
print("result part 2:" + str(result2))
```