from DataStructures.List import array_list as lt
from DataStructures.Priority_queue import pq_entry as pqe

def default_compare_higher_value(father_node, child_node):
    if pqe.get_priority(father_node) >= pqe.get_priority(child_node):
        return True
    return False

def default_compare_lower_value(father_node, child_node):
    if pqe.get_priority(father_node) <= pqe.get_priority(child_node):
        return True
    return False

def is_empty(my_heap):
    return size(my_heap) == 0

def new_heap(is_min_pq=True):
    heap = {
        'elements': lt.new_list(),
        'size': 0,
        'cmp_function': None
    }
    if is_min_pq:
        heap['cmp_function'] = default_compare_lower_value
    else:
        heap['cmp_function'] = default_compare_higher_value

    lt.add_last(heap['elements'], None)

    return heap

def exchange(my_heap, pos1, pos2):
    elements = my_heap['elements']
    e1 = lt.get_element(elements, pos1)
    e2 = lt.get_element(elements, pos2)
    lt.change_info(elements, pos1, e2)
    lt.change_info(elements, pos2, e1)

def swim(my_heap, pos):
    elements = my_heap['elements']

    while pos > 1:
        parent = pos // 2
        current = lt.get_element(elements, pos)
        father = lt.get_element(elements, parent)

        if not priority(my_heap, father, current):
            exchange(my_heap, pos, parent)
            pos = parent 
        else:
            pos = 1 

def remove(my_heap):
    if is_empty(my_heap):
        return None

    elements = my_heap['elements']
    top = lt.get_element(elements, 1)
    exchange(my_heap, 1, my_heap['size'])
    lt.remove_last(elements)
    my_heap['size'] -= 1
    if my_heap['size'] > 0:
        sink(my_heap, 1)
    return pqe.get_value(top)

def contains(my_heap, value):
    return is_present_value(my_heap, value) != -1


def insert(my_heap, priority, value):
    entry = pqe.new_pq_entry(priority, value)
    lt.add_last(my_heap['elements'], entry)
    my_heap['size'] += 1
    swim(my_heap, my_heap['size'])
    return my_heap

def priority(my_heap, parent, child):
    return my_heap["cmp_function"](parent, child)

def size(my_heap):
    return my_heap["size"]

def sink(my_heap, pos):
    elements = my_heap["elements"]
    n = my_heap["size"]
    while 2 * pos <= n:
        child = 2 * pos  
        if child < n:
            left = lt.get_element(elements, child)
            right = lt.get_element(elements, child + 1)

            if not priority(my_heap, left, right):
                child += 1

        child_node = lt.get_element(elements, child)
        parent_node = lt.get_element(elements, pos)

        if priority(my_heap, parent_node, child_node):
            break

        exchange(my_heap, pos, child)
        pos = child
        
def get_first_priority(my_heap):
    if size(my_heap) == 0:
        return None
    first_entry = my_heap["elements"][0]
    return first_entry["value"]

def improve_priority(my_heap, priority, value):
    pos = is_present_value(my_heap, value)
    if pos == -1:
        return my_heap  

    entry = my_heap["elements"][pos]
    old_priority = entry["priority"]

    if my_heap["cmp_function"](priority, old_priority):
        entry["priority"] = priority
        my_heap["elements"][pos] = entry

        swim(my_heap, pos)
        sink(my_heap, pos)

    return my_heap

def is_present_value(my_heap, value):
    elements = my_heap["elements"]
    for i in range(len(elements)):
        if elements[i]["value"] == value:
            return i
    return -1