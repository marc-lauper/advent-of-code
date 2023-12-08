# Day 7 - Camel Cards
See https://adventofcode.com/2023/day/7

## Part 1
```python
import re
from functools import cmp_to_key

NO_VALUE = 0
HIGH_CARD = 1
ONE_PAIR = 2
TWO_PAIRS = 3
THREE_OF_A_KIND = 4
FULL_HOUSE = 5
FOUR_OF_A_KIND = 6
FIVE_OF_A_KIND = 7

class Hand:
    cards = ""
    sorted_cards = ""
    bid = 0
    score = NO_VALUE

def value_of_card(card):
    if(card == 'A'):
        return 14
    elif(card == 'K'):
        return 13
    elif(card == 'Q'):
        return 12
    elif(card == 'J'):
        return 11
    elif(card == 'T'):
        return 10
    else:
        return int(card)

def compare_cards(card1, card2):
    return value_of_card(card1) - value_of_card(card2)
    
def compare_hands(hand1, hand2):
    if(hand1.score != hand2.score):
        return hand1.score - hand2.score
    else:
        for i in range(0, len(hand1.cards)):
            if(hand1.cards[i] != hand2.cards[i]):
                return compare_cards(hand1.cards[i], hand2.cards[i])
        return 0


def DetermineType(cards):
    found_three = re.search(r'(.)\1{2}', cards)
    if found_three:
        if re.search(r'(.)(\1){3}', cards):
            if re.search(r'(.)\1{4}', cards):
                return FIVE_OF_A_KIND
            else:
                return FOUR_OF_A_KIND
        else:
            break_down = cards.replace(found_three.group(1), '')
            if(re.search(r'(.)\1{1}', break_down)):
                return FULL_HOUSE
            return THREE_OF_A_KIND
    else:
        found_two = re.search(r'(.)\1{1}', cards)
        if(found_two):
            break_down = cards.replace(found_two.group(1), '')
            if(re.search(r'(.)\1{1}', break_down)):
                return TWO_PAIRS
            else:
                return ONE_PAIR
        else:
            return HIGH_CARD

hands = []

current_map_name = ""
with open('aoc7.txt', 'r') as file:
    line_number = 0
    for line in file:
        line = line.replace('\n', '')
        
        parsed = re.findall(r'\S+', line)
        if(len(parsed) == 2):
            hand = Hand()
            hand.cards = parsed[0]
            hand.bid = int(parsed[1])
            hand.sorted_cards = ''.join(sorted(hand.cards))
            hand.score = DetermineType(hand.sorted_cards)
            hands.append(hand)

hands = sorted(hands, key=cmp_to_key(compare_hands))
rank = 1
result = 0
for hand in hands:
    value = hand.bid * rank
    result += value
    rank += 1

print("result:" + str(result))
```

## Part 2
```python
import re
from functools import cmp_to_key

NO_VALUE = 0
HIGH_CARD = 1
ONE_PAIR = 2
TWO_PAIRS = 3
THREE_OF_A_KIND = 4
FULL_HOUSE = 5
FOUR_OF_A_KIND = 6
FIVE_OF_A_KIND = 7

class Hand:
    cards = ""
    sorted_cards = ""
    bid = 0
    score = NO_VALUE

def value_of_card(card):
    if(card == 'A'):
        return 14
    elif(card == 'K'):
        return 13
    elif(card == 'Q'):
        return 12
    elif(card == 'J'):
        return 1
    elif(card == 'T'):
        return 10
    else:
        return int(card)

def compare_cards(card1, card2):
    return value_of_card(card1) - value_of_card(card2)
    
def compare_hands(hand1, hand2):
    if(hand1.score != hand2.score):
        return hand1.score - hand2.score
    else:
        for i in range(0, len(hand1.cards)):
            if(hand1.cards[i] != hand2.cards[i]):
                return compare_cards(hand1.cards[i], hand2.cards[i])
        return 0

def DetermineTypeOld(cards):
    found_three = re.search(r'(.)\1{2}', cards)
    if found_three:
        if re.search(r'(.)(\1){3}', cards):
            if re.search(r'(.)\1{4}', cards):
                return FIVE_OF_A_KIND
            else:
                return FOUR_OF_A_KIND
        else:
            break_down = cards.replace(found_three.group(1), '')
            if(re.search(r'(.)\1{1}', break_down)):
                return FULL_HOUSE
            return THREE_OF_A_KIND
    else:
        found_two = re.search(r'(.)\1{1}', cards)
        if(found_two):
            break_down = cards.replace(found_two.group(1), '')
            if(re.search(r'(.)\1{1}', break_down)):
                return TWO_PAIRS
            else:
                return ONE_PAIR
        else:
            return HIGH_CARD


def DetermineType(cards):
    number_of_j = cards.count('J')

    ## JJJJJ ==> Five of a Kind
    ## JJJJA ==> Five of a Kind
    if(number_of_j > 3 ):
        return FIVE_OF_A_KIND

    old_type = DetermineTypeOld(cards.replace('J', ''))
    
    ## JJJAA ==> Five of a Kind
    ## JJJAB ==> Four of a Kind
    if(number_of_j == 3):
        if(old_type == ONE_PAIR):
            return FIVE_OF_A_KIND
        else:
            return FOUR_OF_A_KIND
    
    ## JJAAA ==> Five of a Kind
    ## JJAAB ==> Four of a Kind
    ## JJABC ==> Three of a Kind
    if(number_of_j == 2):
        if(old_type == THREE_OF_A_KIND):
            return FIVE_OF_A_KIND
        elif(old_type == ONE_PAIR):
            return FOUR_OF_A_KIND
        else:
            return THREE_OF_A_KIND
    
    ## JAAAA ==> Five of a Kind
    ## JAAAB ==> Four of a Kind
    ## JAABB ==> Full House
    ## JAABC ==> Three of a Kind
    ## JABCD ==> One Pair
    if(number_of_j == 1):
        if(old_type == FOUR_OF_A_KIND):
            return FIVE_OF_A_KIND
        elif(old_type == THREE_OF_A_KIND):
            return FOUR_OF_A_KIND
        elif(old_type == TWO_PAIRS):
            return FULL_HOUSE
        elif(old_type == ONE_PAIR):
            return THREE_OF_A_KIND
        else:
            return ONE_PAIR
    
    return old_type

hands = []

current_map_name = ""
with open('aoc7.txt', 'r') as file:
    line_number = 0
    for line in file:
        line = line.replace('\n', '')
        parsed = re.findall(r'\S+', line)
        if(len(parsed) == 2):
            hand = Hand()
            hand.cards = parsed[0]
            hand.bid = int(parsed[1])
            # if(hand.cards == 'JJJJJ'):
            #     hand.cards = '11111'
            hand.sorted_cards = ''.join(sorted(hand.cards))
            hand.score = DetermineType(hand.sorted_cards)
            hands.append(hand)

hands = sorted(hands, key=cmp_to_key(compare_hands))
rank = 1
result = 0
for hand in hands:
    value = hand.bid * rank
    result += value
    rank += 1

print("result:" + str(result))
```