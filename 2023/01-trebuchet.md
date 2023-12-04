# Day 1 - Trebuchet?!
See https://adventofcode.com/2023/day/1

## Part 1

```bash
cat aoc1.txt | sed -E 's/[^0-9]//g;s/([0-9]).*?([0-9])/\1\2/g;s/^([0-9])$/\1\1/g' | awk -F'\n' '{sum+=$1;}END{print sum;}'
```

## Part 2
```bash
cat aoc1.txt | sed -E "s/one/o1e/g;s/two/t2o/g;s/three/th3ee/g;s/four/fo4r/g;s/five/fi5ve/g;s/six/s6x/g;s/seven/se7en/g;s/eight/eig8ht/g;s/nine/ni9ne/g;s/[^0-9]//g;s/([0-9]).*?([0-9])/\1\2/g;s/^([0-9])$/\1\1/g" | awk -F'\n' '{sum+=$1;}END{print sum;}'
```
