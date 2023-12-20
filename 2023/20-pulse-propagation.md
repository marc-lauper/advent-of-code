# Day 20 - Pulse Propagation
See https://adventofcode.com/2023/day/20

## Part 1
```python
VERBOSE = False
DEBUG = False

HIGH = True
LOW = False

OFF = False
ON = True

FLIP_FLOP = '%'
CONJUNCTION = '&'
BROADCASTER = 'b'

CYCLES = 1000

def print_verbose(text):
    if VERBOSE:
        print(text)

def print_debug(text):
    if DEBUG:
        print(text)

COUNTERS = {
    HIGH: 0,
    LOW: 0
}

def pulse_to_string(pulse):
    return 'HIGH' if pulse == HIGH else 'LOW'

class Pulse:
    def __init__(self, initiator, target, value):
        self.initiator = initiator
        self.target = target
        self.value = value

class Broadcaster:
    def __init__(self, targets):
        self.name = 'broadcaster'
        self.targets = targets
        
    def processPulse(self, pulse):
        COUNTERS[pulse] += 1
        print_debug(f"Broadcaster received a {pulse_to_string(pulse)} pulse")
        next_pulses = []
        for target in self.targets:
            next_pulses.append(Pulse(self.name, target, pulse))
        return next_pulses
    
    def computeKey(self):
        return ""

class FlipFlop:
    def __init__(self, name, targets):
        self.name = name
        self.status = OFF
        self.targets = targets
        
    def processPulse(self, pulse):
        COUNTERS[pulse.value] += 1
        if pulse.value == HIGH:
            print_debug(f"{pulse.initiator} -{pulse_to_string(pulse.value)}-> {self.name} (ignoring it)")
            return []
        print_debug(f"{pulse.initiator} -{pulse_to_string(pulse.value)}-> {self.name}")
        self.status = not self.status
        pulse_to_send = HIGH if self.status == ON else LOW
        next_pulses = []
        for target in self.targets:
            next_pulses.append(Pulse(self.name, target, pulse_to_send))
        return next_pulses
    
    def computeKey(self):
        return f"{self.name}-{self.status}"

class Conjunction:
    def __init__(self, name, targets):
        self.name = name
        self.targets = targets
        self.inputs = {}
    
    def addInput(self, input):
        self.inputs[input] = LOW

    def processPulse(self, pulse):
        COUNTERS[pulse.value] += 1
        print_debug(f"{pulse.initiator} -{pulse_to_string(pulse.value)}-> {self.name}")
        self.inputs[pulse.initiator] = pulse.value
        all_are_high = True
        for input in self.inputs:
            if self.inputs[input] == LOW:
                all_are_high = False
                break
        pulse_to_send = LOW if all_are_high else HIGH
        next_pulses = []
        for target in self.targets:
            next_pulses.append(Pulse(self.name, target, pulse_to_send))
        return next_pulses
    
    def computeKey(self):
        result = self.name
        for inputName in self.inputs:
            result += f"-{inputName}-{self.inputs[inputName]}"
        return result

class Circuit:
    def __init__(self):
        self.Components = {}
    
    def addComponent(self, component):
        self.Components[component.name] = component
    
    def computeKey(self):
        result = ""
        for component in self.Components:
            result += f"-{self.Components[component].computeKey()}"
        return result
    
    def RegisterInputs(self):
        conjunctions = []
        for component in self.Components:
            if isinstance(self.Components[component], Conjunction):
                conjunctions.append(self.Components[component].name)
        
        for component in self.Components:
            for target in self.Components[component].targets:
                if target in conjunctions:
                    self.Components[target].addInput(component)
    
    def pressKey(self):
        next_pulses = self.Components['broadcaster'].processPulse(LOW)
        while(len(next_pulses) > 0):
            next_pulse = next_pulses.pop(0)
            if(self.Components.get(next_pulse.target) == None):
                COUNTERS[next_pulse.value] += 1
                print_debug(f"{next_pulse.initiator} -{pulse_to_string(next_pulse.value)}-> {next_pulse.target} (ignoring it)")
            else:
                next_pulses += self.Components[next_pulse.target].processPulse(next_pulse)

circuit = Circuit()
key_presses = 0
key_presses_to_reach_circuit = {}
results = []
with open('aoc20.txt', 'r') as file:
    for line in file:
        line = line.replace('\n', '')
        if(len(line) == 0):
            continue
        key, targets = line.split(' -> ')
        targets = targets.split(', ')

        component_type = key[0]
        component_name = key[1:]
        if(component_type == BROADCASTER):
            component = Broadcaster(targets)
        elif(component_type == FLIP_FLOP):
            component = FlipFlop(component_name, targets)
        elif(component_type == CONJUNCTION):
            component = Conjunction(component_name, targets)
        else:
            raise Exception(f"Unknown component type: {component_type}")
        circuit.addComponent(component)

circuit.RegisterInputs()

circuit_key = circuit.computeKey()
print_verbose(f"Circuit key is {circuit_key}")
while(key_presses < CYCLES):
    
    print(f"Processing key press {key_presses} / {CYCLES}", end='\r')
    
    if key_presses_to_reach_circuit.get(circuit_key) != None:
        print(f"Found a loop after {key_presses} key presses")
        loop = key_presses
        remaining_cycles = CYCLES - key_presses
        jump = loop * (remaining_cycles // loop)
        print_debug(f"Jumping {jump} cycles")
        key_presses += jump
        COUNTERS[HIGH] *= (jump/loop)+1
        COUNTERS[LOW] *= (jump/loop)+1
        if(key_presses >= CYCLES):
            break
    
    key_presses_to_reach_circuit[circuit_key] = key_presses
    results.append([COUNTERS[HIGH], COUNTERS[LOW]])
    
    key_presses += 1
    print_debug(f"Key press {key_presses}")
    circuit.pressKey()
    circuit_key = circuit.computeKey()
    print_verbose(f"Circuit key is {circuit_key}")

result = COUNTERS[HIGH] * COUNTERS[LOW]
print(f"\nresult: {COUNTERS[LOW]} * {COUNTERS[HIGH]} = {int(result)}")
```

## Part 2
```python
from math import prod

VERBOSE = False
DEBUG = False

HIGH = True
LOW = False

OFF = False
ON = True

FLIP_FLOP = '%'
CONJUNCTION = '&'
BROADCASTER = 'b'

rx_conditions = {}

def print_verbose(text):
    if VERBOSE:
        print(text)

def print_debug(text):
    if DEBUG:
        print(text)

COUNTERS = {
    HIGH: 0,
    LOW: 0
}

PREDECESSOR = 'ls' # ls is the only input to rx. Might be specific to my input...

def pulse_to_string(pulse):
    return 'HIGH' if pulse == HIGH else 'LOW'

class Pulse:
    def __init__(self, initiator, target, value):
        self.initiator = initiator
        self.target = target
        self.value = value

class Broadcaster:
    def __init__(self, targets):
        self.name = 'broadcaster'
        self.targets = targets
        
    def processPulse(self, pulse):
        COUNTERS[pulse] += 1
        print_debug(f"Broadcaster received a {pulse_to_string(pulse)} pulse")
        next_pulses = []
        for target in self.targets:
            next_pulses.append(Pulse(self.name, target, pulse))
        return next_pulses
    
    def computeKey(self):
        return ""

class FlipFlop:
    def __init__(self, name, targets):
        self.name = name
        self.status = OFF
        self.targets = targets
        
    def processPulse(self, pulse):
        COUNTERS[pulse.value] += 1
        if pulse.value == HIGH:
            print_debug(f"{pulse.initiator} -{pulse_to_string(pulse.value)}-> {self.name} (ignoring it)")
            return []
        print_debug(f"{pulse.initiator} -{pulse_to_string(pulse.value)}-> {self.name}")
        self.status = not self.status
        pulse_to_send = HIGH if self.status == ON else LOW
        next_pulses = []
        for target in self.targets:
            next_pulses.append(Pulse(self.name, target, pulse_to_send))
        return next_pulses
    
    def computeKey(self):
        return f"{self.name}-{self.status}"

class Conjunction:
    def __init__(self, name, targets):
        self.name = name
        self.targets = targets
        self.inputs = {}
    
    def addInput(self, input):
        self.inputs[input] = LOW

    def processPulse(self, pulse):
        COUNTERS[pulse.value] += 1
        print_debug(f"{pulse.initiator} -{pulse_to_string(pulse.value)}-> {self.name}")
        self.inputs[pulse.initiator] = pulse.value
        all_are_high = True
        for input in self.inputs:
            if self.inputs[input] == LOW:
                all_are_high = False
                break
        pulse_to_send = LOW if all_are_high else HIGH
        next_pulses = []
        for target in self.targets:
            next_pulses.append(Pulse(self.name, target, pulse_to_send))
        return next_pulses
    
    def computeKey(self):
        result = self.name
        for inputName in self.inputs:
            result += f"-{inputName}-{self.inputs[inputName]}"
        return result

class Circuit:
    def __init__(self):
        self.Components = {}
    
    def addComponent(self, component):
        self.Components[component.name] = component
    
    def computeKey(self):
        result = ""
        for component in self.Components:
            result += f"-{self.Components[component].computeKey()}"
        return result
    
    def RegisterInputs(self):
        conjunctions = []
        for component in self.Components:
            if isinstance(self.Components[component], Conjunction):
                conjunctions.append(self.Components[component].name)
        
        for component in self.Components:
            for target in self.Components[component].targets:
                if target in conjunctions:
                    self.Components[target].addInput(component)
    
    def pressKey(self, key_presses):
        next_pulses = self.Components['broadcaster'].processPulse(LOW)
        while(len(next_pulses) > 0):
            next_pulse = next_pulses.pop(0)
            
            if(next_pulse.target == PREDECESSOR and next_pulse.value == HIGH):
                rx_conditions[next_pulse.initiator] = key_presses
            
            if(self.Components.get(next_pulse.target) == None):
                COUNTERS[next_pulse.value] += 1
                print_debug(f"{next_pulse.initiator} -{pulse_to_string(next_pulse.value)}-> {next_pulse.target} (ignoring it)")
            else:
                next_pulses += self.Components[next_pulse.target].processPulse(next_pulse)

circuit = Circuit()
with open('aoc20.txt', 'r') as file:
    for line in file:
        line = line.replace('\n', '')
        if(len(line) == 0):
            continue
        key, targets = line.split(' -> ')
        targets = targets.split(', ')

        component_type = key[0]
        component_name = key[1:]
        if(PREDECESSOR in targets):
            rx_conditions[component_name] = 0
        if(component_type == BROADCASTER):
            component = Broadcaster(targets)
        elif(component_type == FLIP_FLOP):
            component = FlipFlop(component_name, targets)
        elif(component_type == CONJUNCTION):
            component = Conjunction(component_name, targets)
        else:
            raise Exception(f"Unknown component type: {component_type}")
        circuit.addComponent(component)

circuit.RegisterInputs()

circuit_key = circuit.computeKey()
print_verbose(f"Circuit key is {circuit_key}")
key_presses = 0
while(True):
    key_presses += 1
    print_debug(f"Key press {key_presses}")
    circuit.pressKey(key_presses)
    circuit_key = circuit.computeKey()
    print_verbose(f"Circuit key is {circuit_key}")
    if(all(rx_conditions.values())):
        print(f"result2: {prod(rx_conditions.values())}")
        exit()
```