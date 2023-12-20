# Day 19 - Aplenty
See https://adventofcode.com/2023/day/19

## Part 1
```python
import re

VERBOSE = False
DEBUG = False
INITIAL_WORKFLOW = 'in'

ACCEPTED = 'A'
REJECTED = 'R'

class Part:
    def __init__(self, x, m, a, s):
        self.data = {
            'x': x,
            'm': m,
            'a': a,
            's': s
        }
        self.value = x + m + a + s

    def __str__(self):
        return f"[x={self.data['x']}, m={self.data['m']}, a={self.data['a']}, s={self.data['s']}]"

    def __repr__(self):
        return str(self)

class Rule:
    var = None
    operation = None
    value = None
    next_rule = None
    
    def matches(self, part):
        if(self.operation == None):
            return True
        elif(self.operation == '<'):
            return part.data[self.var] < self.value
        elif(self.operation == '>'):
            return part.data[self.var] > self.value
        else:
            raise Exception(f"Unknown operation: {self.operation}")

    def __str__(self):
        if(self.operation == None):
            return f"[{self.next_rule}]"
        else:
            return f"[{self.var}{self.operation}{self.value}:{self.next_rule}]"

    def __repr__(self):
        return str(self)

def print_verbose(text):
    if VERBOSE:
        print(text)

def print_verbose(text):
    if VERBOSE:
        print(text)

def print_debug(text):
    if DEBUG:
        print(text)

def should_accept(workflows, part, current_workflow_key):
    i = 0
    for rule in workflows[current_workflow_key]:
        if(rule.matches(part)):
            print_verbose(f"Rule {i} of workflow {current_workflow_key} matches part {part}")
            if(rule.next_rule == ACCEPTED):
                return True
            elif(rule.next_rule == REJECTED):
                return False
            else:
                return should_accept(workflows, part, rule.next_rule)
        else:
            print_verbose(f"Rule {i} of workflow {current_workflow_key} does not match part {part}")
        i =+ 1
        

workflows = {}
parts = []
with open('aoc19.txt', 'r') as file:
    parsing_workflows = True
    for line in file:
        line = line.replace('\n', '')
        if(len(line) == 0):
            parsing_workflows = False
            continue

        if parsing_workflows:
            match = re.search(r'(\w+)\{(.*)\}', line)
            key = match.group(1)
            rules = match.group(2)
            rules = rules.split(',')
            print_debug(f"Adding workflow: {key}")
            workflow = []
            for rule in rules:
                match = re.search(r'(\w+)(?:([<>])(\d+):(\w+)){0,1}', rule)
                var = match.group(1)
                operation = match.group(2)
                value = match.group(3)
                next_rule = match.group(4)
                rule = Rule()
                if(next_rule != None):
                    rule.var = var
                    rule.operation = operation
                    rule.value = int(value)
                    rule.next_rule = next_rule
                else:
                    rule.next_rule = var
                print_debug(f"  {rule}")
                workflow.append(rule)

            workflows[key] = workflow

        else:
            match = re.search(r'\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)\}', line)
            x = int(match.group(1))
            m = int(match.group(2))
            a = int(match.group(3))
            s = int(match.group(4))
            part = Part(x, m, a, s)
            parts.append(part)

result = 0
for part in parts:
    if(should_accept(workflows, part, INITIAL_WORKFLOW)):
        result += part.value

print(f"result: {result}")
```