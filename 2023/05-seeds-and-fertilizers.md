# Day 5 - If You Give A Seed A Fertilizer
See https://adventofcode.com/2023/day/5

## Part 1
```python
import re, sys

class Cell:
    source_range_start = 0
    destination_range_start = 0
    range_length = 0

seeds = []
maps = {}

current_map_name = ""
with open('aoc5.txt', 'r') as file:
    first = True
    for line in file:
        print("Processing line: " + line)
        if(first):
            first = False
            seeds = re.findall(r'\d+', line)
            print("seeds: " + str(seeds))
            continue
        map_name = re.match(r'(.+) map', line)
        if(map_name):
            print("map name: " + map_name.group(1))
            current_map_name = map_name.group(1)
            maps[current_map_name] = []
            continue
        numbers = re.findall(r'\d+', line)
        if(numbers):
            cell = Cell()
            cell.destination_range_start = int(numbers[0])
            cell.source_range_start = int(numbers[1])
            cell.range_length = int(numbers[2])
            maps[current_map_name].append(cell)
            print("    " + str(cell.source_range_start) + " -> " + str(cell.destination_range_start) + " (" + str(cell.range_length) + ")")
            continue


def findInMaps(map, source):
    for nextMapping in maps[map]:
        if(nextMapping.source_range_start <= source and nextMapping.source_range_start + nextMapping.range_length >= source):
            return nextMapping.destination_range_start + (source - nextMapping.source_range_start)
    return source

min_location = sys.maxsize;
for seed in seeds:
    soil = findInMaps("seed-to-soil", int(seed))
    print("  seed " + str(seed) + " -> soil " + str(soil))
    fertilizer = findInMaps("soil-to-fertilizer", soil)
    print("  soil " + str(soil) + " -> fertilizer " + str(fertilizer))
    water = findInMaps("fertilizer-to-water", fertilizer)
    print("  fertilizer " + str(fertilizer) + " -> water " + str(water))
    light = findInMaps("water-to-light", water)
    print("  water " + str(water) + " -> light " + str(light))
    temperature = findInMaps("light-to-temperature", light)
    print("  light " + str(light) + " -> temperature " + str(temperature))
    humidity = findInMaps("temperature-to-humidity", temperature)
    print("  temperature " + str(temperature) + " -> humidity " + str(humidity))
    location = findInMaps("humidity-to-location", humidity)
    print("  humidity " + str(humidity) + " -> location " + str(location))
    print("seed " + str(seed) + " -> location " + str(location))
    if(location < min_location):
        min_location = location

print("result:" + str(min_location))
```

# Part 2
Is it elegant, or even fast? No. But it works, and I had more important things to do than optimize it.
```python
import re, sys, time

class Cell:
    source_range_start = 0
    destination_range_start = 0
    range_length = 0

class SeedRange:
    start = 0
    length = 0

seeds_ranges = []
maps = {}

current_map_name = ""
total_seeds = 0
with open('aoc5.txt', 'r') as file:
    first = True
    for line in file:
        if(first):
            first = False
            seed_ranges = re.findall(r'(\d+ \d+)', line)
            # print("seeds ranges: " + str(seed_ranges))
            for seed_range in seed_ranges:
                seeds_start =int(seed_range.split(' ')[0])
                seeds_range = int(seed_range.split(' ')[1])
                new_range = SeedRange()
                new_range.start = seeds_start
                new_range.length = seeds_range
                seeds_ranges.append(new_range)
                total_seeds += seeds_range
            continue
        map_name = re.match(r'(.+) map', line)
        if(map_name):
            current_map_name = map_name.group(1)
            maps[current_map_name] = []
            continue
        numbers = re.findall(r'\d+', line)
        if(numbers):
            cell = Cell()
            cell.destination_range_start = int(numbers[0])
            cell.source_range_start = int(numbers[1])
            cell.range_length = int(numbers[2])
            maps[current_map_name].append(cell)
            continue

def reverseLookupInMaps(map, destination):
    for nextMapping in maps[map]:
        if(nextMapping.destination_range_start <= destination and nextMapping.destination_range_start + nextMapping.range_length >= destination):
            return nextMapping.source_range_start + (destination - nextMapping.destination_range_start)
    return destination


min_location = None;
i = 0
size = 100
step_size = 1
start = time.time()
min_range = None
maps["humidity-to-location"] = sorted(maps["humidity-to-location"], key=lambda x: x.destination_range_start)

count_locations = 0
for next_range in maps["humidity-to-location"]:
    count_locations += next_range.range_length


for next_range in maps["humidity-to-location"]:
    for location in range(next_range.destination_range_start, next_range.destination_range_start + next_range.range_length, step_size):
        humidity = reverseLookupInMaps("humidity-to-location", location)
        temperature = reverseLookupInMaps("temperature-to-humidity", humidity)
        light = reverseLookupInMaps("light-to-temperature", temperature)
        water = reverseLookupInMaps("water-to-light", light)
        fertilizer = reverseLookupInMaps("fertilizer-to-water", water)
        soil = reverseLookupInMaps("soil-to-fertilizer", fertilizer)
        seed = reverseLookupInMaps("seed-to-soil", soil)
        for seed_range in seeds_ranges:
            if(seed >= seed_range.start and seed < seed_range.start + seed_range.length):
                if(min_location == None or location < min_location):
                    min_location = location
                    min_range = next_range
                    print("result: " + str(min_location) + " (seed: " + str(seed) + ")")
                    exit()
                break
        i += step_size
        percent = (i * 100) / count_locations

        x = int(size*i/count_locations)
        remaining = ((time.time() - start) / i) * (count_locations - i)
        
        mins, sec = divmod(remaining, 60)
        hours, mins = divmod(mins, 60)
        days, hours = divmod(hours, 24)
        time_str = f"{int(days):02} days, {int(hours):02} hours, {int(mins):02} minutes and {sec:05.2f} seconds (current min_location: {min_location})"
        
        print(f"[{u'█'*x}{('.'*(size-x))}] {location} ({percent:03.2f} %) Est wait {time_str}", end='\r', file=sys.stdout, flush=True)

print("result:" + str(min_location))
```