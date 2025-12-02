from DataStructures.Tree import rbt_node as nd
from DataStructures.List import single_linked_list as sl
from DataStructures.Tree import binary_search_tree as by
def new_map():
    my_rbt={"root":None,
            "type": "RBT"}
    return my_rbt

def size_tree(root):
    if root==None:
        return 0
    elif root["left"]==None and root["right"]==None:
        return 1
    elif root["left"]!= None and root["right"]!= None:
        return 1+size_tree(root["left"])+size_tree(root["right"])
    elif root["left"]!= None and root["right"]== None:
        return 1+size_tree(root["left"])
    elif root["left"]== None and root["right"]!= None:
        return 1+size_tree(root["right"])

def size(my_rbt):
    return size_tree(my_rbt["root"])

def default_compare(key, element):
    if key > element["key"]:
        return 1
    if key < element["key"]:
        return -1
    else: 
        return 0

def contains(my_rbt, key):    
    value = get(my_rbt, key)
    return value is not None


def is_empty(my_rbt):    
    return size(my_rbt) == 0


def value_set(my_rbt):   
    lista = sl.new_list()
    value_set_tree(my_rbt["root"], lista)
    return lista


def value_set_tree(root, key_list):    
    if root is not None:
        value_set_tree(root["left"], key_list)
        sl.add_last(key_list, root["value"])
        value_set_tree(root["right"], key_list)


def get_max(my_rbt):    
    if my_rbt is None or my_rbt["root"] is None:
        return None
    max_node = get_max_node(my_rbt["root"])
    return nd.get_key(max_node)


def get_max_node(root):    
    if root is None:
        return None
    while root["right"] is not None:
        root = root["right"]
    return root


def keys(my_rbt, key_initial, key_final):    
    lista = sl.new_list()
    keys_range(my_rbt["root"], key_initial, key_final, lista)
    return lista


def keys_range(root, key_initial, key_final, list_key):    
    if root is None:
        return
    if root["key"] > key_initial:
        keys_range(root["left"], key_initial, key_final, list_key)
    if key_initial <= root["key"] <= key_final:
        sl.add_last(list_key, root["key"])
    if root["key"] < key_final:
        keys_range(root["right"], key_initial, key_final, list_key)
        
def put(my_rbt, key, value): 
    my_rbt["root"]=insert_node(my_rbt["root"],key,value) 
    my_rbt["root"]["color"] = "BLACK" 
    return my_rbt 

def rotate_left(node_rbt): 
    derecho=node_rbt["right"] 
    nieto=derecho["left"] 
    derecho["left"]=node_rbt 
    node_rbt["right"]=nieto 
    color=derecho["color"]
    derecho["color"]=node_rbt["color"]
    node_rbt["color"]=color
    return derecho 

def rotate_right(node_rbt): 
    izquierdo=node_rbt["left"] 
    nieto=izquierdo["right"] 
    izquierdo["right"]=node_rbt 
    node_rbt["left"]=nieto 
    color=izquierdo["color"]
    izquierdo["color"]=node_rbt["color"]
    node_rbt["color"]=color
    return izquierdo 

def flip_node_color(nodo): 
    if is_red(nodo): 
        nodo=nd.change_color(nodo, "BLACK") 
    else: 
        nodo=nd.change_color(nodo, "RED") 
    return nodo 

def flip_colors(nodo): 
    nd.change_color(nodo, "RED") 
    if nodo["left"]:
        nd.change_color(nodo["left"], "BLACK") 
    if nodo["right"]:
        nd.change_color(nodo["right"], "BLACK") 
    return nodo 

def is_red(node_rbt): 
    if node_rbt is None: 
        return False 
    return nd.is_red(node_rbt) 

def insert_node(root, key, value): 
    if root==None: 
        return nd.new_node(key, value) 
    else: 
        cmp=default_compare(key, root) 
        if cmp==-1: 
            root["left"] =insert_node(root["left"],key,value) 
        elif cmp==1: 
            root["right"] =insert_node(root["right"],key,value)
        else: 
            root["value"]=value 
        
    if is_red(root["right"]) and not is_red(root["left"]):
        root = rotate_left(root)
    if is_red(root["left"]) and is_red(root["left"]["left"]):
        root = rotate_right(root)
    if is_red(root["left"]) and is_red(root["right"]):
        flip_colors(root)
    return root


def get_node(my_rbt, key):
    node = my_rbt["root"]
    while node is not None:
        if key == node["key"]:
            return node
        elif key < node["key"]:
            node = node["left"]
        else:
            node = node["right"]
    return None

def get(my_rbt, key):
    node = get_node(my_rbt, key)
    if node is not None:
        return node["value"]
    return None

def key_set(my_rbt):
    key_list = sl.new_list()
    key_set_tree(my_rbt["root"], key_list)
    return key_list

def key_set_tree(root, key_list):
    if root is not None:
        key_set_tree(root["left"], key_list)
        sl.add_last(key_list, root["key"])
        key_set_tree(root["right"], key_list)
        
def get_min(my_rbt):
    if my_rbt is None or my_rbt.get("root") is None:
        return None
    node = my_rbt["root"]
    return get_min_node(node)

def get_min_node(node):
    if node is None:
        return None
    current = node
    while current.get("left") is not None:
        current = current["left"]
    return current.get("key")

def height(root):
    res=by.height(root)
    return res

def values(my_rbt, key_initial, key_final):
    value_list = sl.new_list()
    values_range(my_rbt["root"], key_initial, key_final, value_list)
    return value_list

def values_range(root, key_initial, key_final, value_list):
    if root is None:
        return None
    
    if key_initial < root["key"]:
        values_range(root["left"], key_initial, key_final, value_list)
    
    if key_initial <= root["key"] <= key_final:
        sl.add_last(value_list, root["value"])
    
    if key_final > root["key"]:
        values_range(root["right"], key_initial, key_final, value_list)