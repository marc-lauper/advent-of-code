import re, math, os;

VERBOSE = True
DEBUG = False
PLAY_THE_TESTS = False

A = 0
B = 1
C = 2

registers = [0, 0, 0]
instruction_pointer = 0
output = []
expected = []

def reset():
    global registers, instruction_pointer, output
    registers = [0, 0, 0]
    instruction_pointer = 0
    output = []

def play(program):
    global registers, output, expected

    print_verbose("Playing program")
    initial_registers = registers.copy()
    step = 1
    value = step
    biggest = 0

    while True:
        try:
            try_to_play(program, value)
            if output == expected:
                return value
        except Exception as e:
            print_debug(f"Error: {e}")
        
        if(len(output) > biggest):
            print_verbose(f"[{value}] {output}")
            biggest = len(output)
            value *= 10
        else:
            value += step
        reset()
        registers = initial_registers.copy()

def try_to_play(program, register_a):
    global expected, registers

    # print(f"Trying A = {register_a}", end='\r')
    registers[A] = register_a
    print_debug(f"registers: {registers}")
    print_debug(f"program: {program}")
    expected = list(map(int, program.split(',')))
    while True:
        opcode, operand = read_next_opcode(expected)
        if opcode is None:
            break
        execute_instruction(opcode, operand)

def read_next_opcode(program):
    global instruction_pointer
    
    operand_position = instruction_pointer + 1
    if operand_position >= len(program):
        return None, None
    
    opcode = program[instruction_pointer]
    operand = program[operand_position]
    return opcode, operand

def literal_operand(operand):
    return operand

def combo_operand(operand):
    val = None
    if operand < 4:
        val =  operand
        print_debug(f"Combo operand: {operand} => {val}")
    elif operand > 6:
        raise Exception(f"Invalid operand: {operand}")
    else:
        register_index = operand - 4
        val = registers[register_index]
        print_debug(f"Combo operand: {operand} => {val} (from register {register_index})")
    return val

def execute_instruction(instruction, operand):
    global instruction_pointer
    global expected

    pointer_before = instruction_pointer
    match instruction:
        case 0: # adv
            numerator = registers[A]
            denominator = pow(2, combo_operand(operand))
            registers[A] = math.trunc(numerator // denominator)
            print_debug(f"[adv {operand}]: {numerator} // {denominator} => A = {registers[A]}")

        case 1: # bxl
            before = registers[B]
            registers[B] = before ^ literal_operand(operand)
            print_debug(f"[bxl {operand}]: {before} ^ {operand} => B = {registers[B]}")

        case 2: # bst
            combo = combo_operand(operand)
            registers[B] = combo % 8
            print_debug(f"[bst {operand}]: {combo} % 8 => B = {registers[B]}")
        
        case 3: # jnz
            do_nothing = registers[A] == 0
            if do_nothing:
                print_debug(f"[jnz {operand}]: A = {registers[A]} == 0, skipping")
            else:
                instruction_pointer = literal_operand(operand)
                print_debug ("[jnz {operand}]: Instruction pointer set to {instruction_pointer}")

        case 4: # bxc
            value_b = registers[B]
            value_c = registers[C]
            registers[B] = value_b ^ value_c
            print_debug(f"[bxc {operand}]: {value_b} ^ {value_c} => B = {registers[B]}")
        
        case 5: # out
            combo = combo_operand(operand)
            value = combo % 8
            index = len(output)
            expected_value = expected[index]
            output.append(value)
            print_debug(f"[out {operand}]: {combo} % 8 => Outputting {value}")
            if value != expected_value:
                raise Exception(f"Output value {value} does not match expected value {expected_value} at position {index}")


        case 6: # bdv
            numerator = registers[A]
            denominator = pow(2, combo_operand(operand))
            registers[B] = math.trunc(numerator // denominator)
            print_debug(f"[adv {operand}]: {numerator} // {denominator} => B = {registers[B]}")
        
        case 7: # cdv
            numerator = registers[A]
            denominator = pow(2, combo_operand(operand))
            registers[C] = math.trunc(numerator // denominator)
            print_debug(f"[adv {operand}]: {numerator} // {denominator} => C = {registers[C]}")

        case _:
            raise Exception(f"Instruction {instruction} not implemented")
    
    if instruction_pointer == pointer_before:
        instruction_pointer += 2
        print_debug ("Instruction pointer incrementing by 2")

    print_debug(f"Registers: {registers}")
    print_debug(f"Instruction pointer: {instruction_pointer}")
    print_debug(f"Output: {output}")
    print_debug("")

def print_verbose(text):
    if VERBOSE:
        print(text)

def print_debug(text):
    if DEBUG:
        print(text)

def do_some_tests():
    
    if not PLAY_THE_TESTS:
        return

    reset()
    registers[C] = 9
    play("2,6")
    assert registers[B] == 1

    reset()
    registers[A] = 10
    play("5,0,5,1,5,4")
    assert output == [0, 1, 2]

    reset()
    registers[A] = 2024
    play("0,1,5,4,3,0")
    assert output == [4,2,5,6,7,7,7,7,3,1,0]
    assert registers[A] == 0

    reset()
    registers[B] = 29
    play("1,7")
    assert registers[B] == 26

    reset()
    registers[B] = 2024
    registers[C] = 43690
    play("4,0")
    assert registers[B] == 44354

with open(os.path.dirname(os.path.abspath(__file__)) + '/input.txt', 'r') as file:
    result = 0

    # Some tests
    do_some_tests()
    reset()

    for line in file:
        line = line.replace('\n', '')
        if len(line) == 0:
            continue

        match = re.match(r"Register (\w): (\d+)", line)
        if match:
            register = match.group(1)
            value = int(match.group(2))
            registers[ord(register) - ord('A')] = int(value)
            continue
        
        # Parse the following (separating by comma to create an array)
        # Program: 2,4,1,3,7,5,4,2,0,3,1,5,5,5,3,0
        match = re.match(r"Program: (.+)", line)
        if match:
            program = match.group(1)

    # result is the comma-separated output
    result = play(program)

    print (f"\nresult: {result}")


# [1] [7]
# [12] [2, 7]
# [703] [2, 4, 1, 7]
# [8895] [2, 4, 1, 3, 5]
# [268960] [2, 4, 1, 3, 7, 7]
# [2707053] [2, 4, 1, 3, 7, 5, 1]
# [56582847] [2, 4, 1, 3, 7, 5, 4, 1]
# [739335789] [2, 4, 1, 3, 7, 5, 4, 2, 2]