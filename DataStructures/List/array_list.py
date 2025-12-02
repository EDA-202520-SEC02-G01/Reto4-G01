def new_list():
    newlist={"elements": [], "size": 0}
    return newlist

def get_element(my_list, index):
    return my_list["elements"][index]

def is_present(my_list, element, cmp_function):
    size=my_list["size"]
    if size >0 :
        keyexist=False
        for keypos in range(0,size):
            info=my_list["elements"][keypos]
            if cmp_function(element, info)==0:
                keyexist=True
                break 
        if keyexist:
            return keypos
    return -1

def add_first(my_list,elements):
    my_list["elements"].insert(0,elements)
    my_list["size"]+=1
    return my_list

def add_last(my_list,elements):
    my_list["elements"].append(elements)
    my_list["size"]+=1
    return my_list

def size(my_list):
    res=my_list["size"]
    return res

def first_element(my_list):
    element=my_list['elements'][0]
    return element

def is_empty(my_list):
    res=False
    if my_list["size"]==0:
        res = True
    return res

def last_element(my_list):
    last=my_list["elements"][-1]
    return last

def delete_element(my_list, pos):
    my_list["elements"].pop(pos)
    my_list["size"]-=1
    return my_list

def remove_first(my_list):
    element=my_list["elements"].pop(0)
    my_list["size"]-=1
    return element

def remove_last(my_list):
    element=my_list["elements"].pop(-1)
    my_list["size"]-=1
    return element

def insert_element(my_list, pos, element):
    my_list["elements"].insert(pos,element)
    my_list["size"]+=1
    return my_list

def change_info(my_list,pos,new_info):
    my_list["elements"][pos]=new_info
    return my_list

def exchange(my_list, pos_1, pos_2):
    c1=my_list["elements"][pos_1]
    c2=my_list["elements"][pos_2]
    my_list["elements"][pos_1]=c2
    my_list["elements"][pos_2]=c1
    return my_list

def sub_list(my_list, pos_i, num_elements):
    elements = my_list["elements"]
    end_pos = pos_i + num_elements
    if end_pos <= len(elements):
        res = elements[pos_i:end_pos]
        return {"size": len(res), "elements": res}