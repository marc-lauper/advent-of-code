# Day 3 - Gear Ratios
See https://adventofcode.com/2023/day/3

```python
import uuid

class Cell:
    isSymbol = False
    isNumber = False
    mustKeep = False
    value = '.'
    cumulatedValue = 0
    uniqueId = 0
    gearRatio = 0


data = [];
val_per_uuid = {}
with open('aoc3.txt', 'r') as file:
    for line in file:
        # For eveyr character on the line, create a new Cell objec whose value is the character
        row = []
        for character in line:
            if(character == '\n'):
                continue
            cell = Cell()
            cell.value = character
            if(character >= '0' and character <= '9'):
                cell.isNumber = True
            elif(character != '.'):
                cell.isSymbol = True
            row.append(cell)
        data.append(row)

# Verifies if at least one call around this one is a symbol (including diagonals)
def isSurroundedByASymbol(row, col):
    if(row > 0 and data[row - 1][col].isSymbol):
        return True
    if(row < len(data) - 1 and data[row + 1][col].isSymbol):
        return True
    if(col > 0 and data[row][col - 1].isSymbol):
        return True
    if(col < len(data[row]) - 1 and data[row][col + 1].isSymbol):
        return True
    if(row > 0 and col > 0 and data[row - 1][col - 1].isSymbol):
        return True
    if(row > 0 and col < len(data[row]) - 1 and data[row - 1][col + 1].isSymbol):
        return True
    if(row < len(data) - 1 and col > 0 and data[row + 1][col - 1].isSymbol):
        return True
    if(row < len(data) - 1 and col < len(data[row]) - 1 and data[row + 1][col + 1].isSymbol):
        return True
    return False
    
    
# Verifies if we must keep a number cell (e.g. some cells from this number are surrounded by symbols)
def updateMustKeep(row, col):
    if(data[row][col].mustKeep):
        return
    if(not data[row][col].isNumber):
        return
    if(col > 0 and data[row][col - 1].mustKeep):
        data[row][col].mustKeep = True
        data[row][col].uniqueId = data[row][col - 1].uniqueId
        return
    if(isSurroundedByASymbol(row, col)):
        data[row][col].mustKeep = True
        data[row][col].uniqueId = uuid.uuid4()
        return
    if(col < len(data[row]) - 1):
        updateMustKeep(row, col + 1)
        if(data[row][col + 1].mustKeep):
            data[row][col].mustKeep = True
            data[row][col].uniqueId = data[row][col + 1].uniqueId
            return

def updateValue(row, col):
    if(not data[row][col].isNumber):
        return
    if(not data[row][col].mustKeep):
        return
    if(col > 0 and data[row][col-1].isNumber):
        data[row][col].cumulatedValue = data[row][col-1].cumulatedValue * 10 + int(data[row][col].value)
        data[row][col-1].cumulatedValue = 0
        val_per_uuid[data[row][col].uniqueId] = data[row][col].cumulatedValue
    else:
        data[row][col].cumulatedValue = int(data[row][col].value)
        val_per_uuid[data[row][col].uniqueId] = data[row][col].cumulatedValue

# Look for uuids in the surrounding cells (including diagonals). If there are exactly 2, then this is a gear cell and the gearValue is the sum of the values associated to the two uuids
def updateGearValue(row, col):
    if(not data[row][col].value == '*'):
        return
    neighbouring_values = {}
    if(row > 0 and data[row - 1][col].mustKeep):
        neighbouring_values[data[row - 1][col].uniqueId] = val_per_uuid[data[row - 1][col].uniqueId]
    if(row < len(data) - 1 and data[row + 1][col].mustKeep):
        neighbouring_values[data[row + 1][col].uniqueId] = val_per_uuid[data[row + 1][col].uniqueId]
    if(col > 0 and data[row][col - 1].mustKeep):
        neighbouring_values[data[row][col-1].uniqueId] = val_per_uuid[data[row][col-1].uniqueId]
    if(col < len(data[row]) - 1 and data[row][col + 1].mustKeep):
        neighbouring_values[data[row][col+1].uniqueId] = val_per_uuid[data[row][col+1].uniqueId]
    if(row > 0 and col > 0 and data[row - 1][col - 1].mustKeep):
        neighbouring_values[data[row-1][col-1].uniqueId] = val_per_uuid[data[row-1][col-1].uniqueId]
    if(row > 0 and col < len(data[row]) - 1 and data[row - 1][col + 1].mustKeep):
        neighbouring_values[data[row-1][col+1].uniqueId] = val_per_uuid[data[row-1][col+1].uniqueId]
    if(row < len(data) - 1 and col > 0 and data[row + 1][col - 1].mustKeep):
        neighbouring_values[data[row+1][col-1].uniqueId] = val_per_uuid[data[row+1][col-1].uniqueId]
    if(row < len(data) - 1 and col < len(data[row]) - 1 and data[row + 1][col + 1].mustKeep):
        neighbouring_values[data[row+1][col+1].uniqueId] = val_per_uuid[data[row+1][col+1].uniqueId]
    if(len(neighbouring_values) == 2):
        values = list(neighbouring_values.values())
        data[row][col].gearRatio = values[0] * values[1]

result1 = 0
result2 = 0
for row in range(len(data)):
    for col in range(len(data[row])):
        updateMustKeep(row, col)
        updateValue(row, col)

for row in range(len(data)):
    for col in range(len(data[row])):
        updateGearValue(row, col)

for row in range(len(data)):
    for col in range(len(data[row])):
        if(data[row][col].mustKeep and data[row][col].cumulatedValue > 0):
            result1 += data[row][col].cumulatedValue
        if(data[row][col].gearRatio > 0):
            result2 += data[row][col].gearRatio

print("result1:" + str(result1))
print("result2:" + str(result2))
```