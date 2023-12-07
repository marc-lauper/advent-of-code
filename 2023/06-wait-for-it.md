# Day 6 - Wait For It
See https://adventofcode.com/2023/day/6

## Part 1
```python
import re, math

times = []
goals = []
results = []

current_map_name = ""
with open('aoc6.txt', 'r') as file:
    line_number = 0
    for line in file:
        if(line_number == 0):
            times = re.findall(r'\d+', line)
        elif(line_number == 1):
            goals = re.findall(r'\d+', line)
        line_number+=1

i = 0
for i in range(0, len(times)):
    time = int(times[i])
    goal = int(goals[i])
    # Find the smallest x where (time-x)*x = goal
    # time*x - x*x = goal
    # x*x - time*x + goal = 0
    # This is a quadratic equation (b**2 - 4*a*c = 0)
    # a = 1
    # b = -time
    # c = goal
    # x = (-b +/- sqrt(b**2 - 4*a*c)) / (2*a)
    # x = (time +/- sqrt(time**2 - 4*goal)) / 2
    root_discriminant = math.sqrt(pow(time, 2) - 4*goal)
    x = math.ceil((time - root_discriminant) / 2)
    y = math.floor((time + root_discriminant) / 2)
    tmp = (time-x)*x
    if(tmp == goal):
        x = x+1
        y = y-1
    result = y - x + 1

    results.append(result)

end_result = 1
for result in results:
    end_result *= result
print("result:" + str(end_result))
```

## Part 2
The input file was so small, I manually removed the kerning and re-ran the same code...
