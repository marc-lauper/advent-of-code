
# Day 15 - Lens Library
See https://adventofcode.com/2023/day/15

## Part 1
```python
import string

def prepare_reference():
    result = []
    for current_hash in range(256):
        references_for_this_hash = {}
        for new_char in string.printable:
            val = ((current_hash + ord (new_char)) * 17) % 256
            references_for_this_hash[new_char] = val
        result.append(references_for_this_hash)
    return result

reference = prepare_reference()

def hash_step(step):
    result = 0
    for next_char in step:
        result = reference[result][next_char]
    return result

result = 0
with open('aoc15.txt', 'r') as file:
    for line in file:
        line = line.replace('\n', '')
        if(len(line) == 0):
            continue

        steps = line.split(',')
        for step in steps:
            val = hash_step(step)
            result += val

print(f"result: {result}")
```

## Part 2
```python
import string

VERBOSE = False
DEBUG = False

class Lens:
    def __init__(self, label, focal_length):
        self.label = label
        self.focal_length = focal_length

    def __str__(self):
        return f"[{self.label} {self.focal_length}]"

    def __repr__(self):
        return str(self)

class Box:
    def __init__(self, label):
        self.label = label
        self.lenses = []
        self.label_to_position = {}

    def __str__(self):
        lenses_str = []
        for lens in self.lenses:
            lenses_str.append(str(lens))
        return f"Box {self.label}: {' '.join(lenses_str)}"

    def __repr__(self):
        return str(self)

def print_verbose(text):
    if VERBOSE:
        print(text)
        

def print_debug(text):
    if DEBUG:
        print(text)

def prepare_reference():
    result = []
    for current_hash in range(256):
        references_for_this_hash = {}
        for new_char in string.printable:
            val = ((current_hash + ord (new_char)) * 17) % 256
            references_for_this_hash[new_char] = val
        result.append(references_for_this_hash)
    return result

reference = prepare_reference()

def hash_step(step):
    result = 0
    for next_char in step:
        result = reference[result][next_char]
    return result

label_to_box = {}

def prepare_boxes():
    result = []
    for i in range(256):
        box = Box(i)
        result.append(box)
    return result

boxes = prepare_boxes()

def get_box(label):
    if(label in label_to_box):
        return label_to_box[label]
    else:
        box = hash_step(label)
        label_to_box[label] = box
        return box

def update_boxes(step):

    if(step[-1] == '-'):
        label = step[:-1]
        box = get_box(label)
        if(label in boxes[box].label_to_position):
            position = boxes[box].label_to_position[label]
            boxes[box].lenses[position] = None
            del boxes[box].label_to_position[label]

    else:
        split = step.split('=')
        label = split[0]
        focal_length = int(split[1])
        box = get_box(label)
        if(label in boxes[box].label_to_position):
            position = boxes[box].label_to_position[label]
            boxes[box].lenses[position].focal_length = focal_length
        else:
            position = len(boxes[box].lenses)
            boxes[box].lenses.append(Lens(label, focal_length))
            boxes[box].label_to_position[label] = position

with open('aoc15.txt', 'r') as file:
    for line in file:
        line = line.replace('\n', '')
        if(len(line) == 0):
            continue

        steps = line.split(',')
        for step in steps:
            update_boxes(step)
            print_verbose(f"After \"{step}\":")
            for box in boxes:
                if(len(box.lenses) > 0):
                    print_verbose(box)
            print_verbose("")
        
    result = 0
    for box_index in range(len(boxes)):
        print(f"Processing step {box_index + 1} / {len(boxes)}")
        box = boxes[box_index]
        box.lenses = list(filter(None, box.lenses))
        for lens_index in range(len(box.lenses)):
            lens = box.lenses[lens_index]
            res = (box_index + 1) * (lens_index + 1) * lens.focal_length
            print_verbose(f"- {(box_index + 1)} (box {box_index}) * {(lens_index + 1)} (slot {lens_index}) * {lens.focal_length} (focal length) = {res}")
            result += res

print(f"result: {result}")
```