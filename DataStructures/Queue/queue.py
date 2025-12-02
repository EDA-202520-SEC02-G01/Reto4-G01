from DataStructures.List import single_linked_list as lt
def enqueue(my_queue, element):
    lt.add_last(my_queue,element)
    return my_queue

def dequeue(my_queue):
    return lt.delete_element(my_queue,0)

def new_queue():
    return lt.new_list()

def is_empty(my_queue):
    return lt.is_empty(my_queue)

def size(queue):
    return lt.size(queue)

def peek(queue):
    return lt.first_element(queue)