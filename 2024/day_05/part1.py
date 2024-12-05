import re;

VERBOSE = False
DEBUG = False

def print_verbose(text):
    if VERBOSE:
        print(text)
        

def print_debug(text):
    if DEBUG:
        print(text)

def get_middle_page_if_update_is_valid(update, pages_after):
    pages_before = []
    for i in range(len(update)):
        page = update[i]
        if pages_after.get(page):
            print_verbose(f"page: {page}, ordering_rules: {pages_after[page]}, pages_before: {pages_before}")
        else:
            print_verbose(f"page: {page}, no ordering rules")
            pages_before.append(page)
            continue
        
        # Check if pages_before contains any of the pages in ordering_rules[page]
        for page_after in pages_after[page]:
            if page_after in pages_before:
                print_verbose(f"[{update}] page {page_after}, should come after {page}, update is invalid")
                print_verbose(f"[ADDING] 0")
                return 0
        
        pages_before.append(page)
        
    # Find the element in the middle of the "update" list
    middle_index = len(update) // 2
    middle_page = update[middle_index]
    print_verbose(f"[ADDING] {middle_page}")
    return int(middle_page)

with open('input.txt', 'r') as file:
    result = 0
    
    # ordering_rules is a hashmap
    pages_after = {}
    
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
    
    for update in updates:
        result += get_middle_page_if_update_is_valid(update, pages_after)
            
            
        
    
    print (f"result: {result}")
