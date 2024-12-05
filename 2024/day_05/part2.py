import re;
from functools import cmp_to_key;

VERBOSE = False
DEBUG = False
# ordering_rules is a hashmap
pages_after = {}
    

def print_verbose(text):
    if VERBOSE:
        print(text)
        

def print_debug(text):
    if DEBUG:
        print(text)

def get_incorrectly_ordered(update):
    pages_before = []
    for i in range(len(update)):
        page = update[i]
        if pages_after.get(page):
            print_debug(f"page: {page}, ordering_rules: {pages_after[page]}, pages_before: {pages_before}")
        else:
            print_debug(f"page: {page}, no ordering rules")
            pages_before.append(page)
            continue
        
        # Check if pages_before contains any of the pages in ordering_rules[page]
        for page_after in pages_after[page]:
            if page_after in pages_before:
                print_debug(f"[{update}] page {page_after}, should come after {page}, update is invalid")
                return update
        
        pages_before.append(page)
        
    return None

def compare(page1, page2):
    if pages_after.get(page1) and page2 in pages_after[page1]:
            return -1
    if pages_after.get(page2) and page1 in pages_after[page2]:
            return 1
    return 0

def make_valid_and_get_middle_page(update):
    
    # Sort "update" based on the ordering rules
    update = sorted(update, key=cmp_to_key(compare))
    
    # Find the element in the middle of the "update" list
    middle_index = len(update) // 2
    middle_page = update[middle_index]
    print_verbose(f"[ADDING] {middle_page}")
    return int(middle_page)

with open('input.txt', 'r') as file:
    result = 0
    
    # updates is a list of list
    updates = []

    for line in file:
        if(len(line) < 2):
            continue
        # Does it match \d+\|\d+ ?
        is_ordering_rule = re.match(r'(\d+)\|(\d+)', line)
        if is_ordering_rule:
            rules = is_ordering_rule.groups()
            print_debug(f"ordering rule: {rules}")
            if(pages_after.get(rules[0])):
                pages_after[rules[0]].append(rules[1])
            else:
                pages_after[rules[0]] = [rules[1]]
            continue
        update = re.findall(r',?(\d+)', line)
        if update:
            print_debug(f"update: {update}")
            updates.append(update)
            continue
    
    incorrectly_ordered = []
    for update in updates:
        is_incorrectly_ordered = get_incorrectly_ordered(update)
        if is_incorrectly_ordered:
            incorrectly_ordered.append(is_incorrectly_ordered)
    
    for update in incorrectly_ordered:
        print_verbose(f"incorrectly ordered: {update}")
        result += make_valid_and_get_middle_page(update)
    
    print (f"result: {result}")
