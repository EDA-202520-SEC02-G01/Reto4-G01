from DataStructures.List import array_list as al
from DataStructures.Map import map_entry as me
from DataStructures.Map import map_functions as mf

def find_slot(my_map, key, hash_value):
   first_avail = None
   found = False
   ocupied = False
   while not found:
      if is_available(my_map["table"], hash_value):
            if first_avail is None:
               first_avail = hash_value
            entry = al.get_element(my_map["table"], hash_value)
            if me.get_key(entry) is None:
               found = True
      elif default_compare(key, al.get_element(my_map["table"], hash_value)) == 0:
            first_avail = hash_value
            found = True
            ocupied = True
      hash_value = (hash_value + 1) % my_map["capacity"]
   return ocupied, first_avail


def is_available(table, pos):
    
   entry = al.get_element(table, pos)
   if me.get_key(entry) is None or me.get_key(entry) == "__EMPTY__":
      return True
   return False


def default_compare(key, entry):

   if key == me.get_key(entry):
      return 0
   elif key > me.get_key(entry):
      return 1
   return -1


def put(my_map, key, value):
    valor=mf.hash_value(my_map,key)
    estado,pos=find_slot(my_map,key,valor)
    if estado:
        my_map["table"]["elements"][pos]["value"]=value
    else: 
        my_map["table"]["elements"][pos]["key"]=key
        my_map["table"]["elements"][pos]["value"]=value
        
        my_map["size"] += 1
        elementos=my_map["current_factor"]* my_map["capacity"]
        curren_factor=(elementos+1)/my_map["capacity"]
        if curren_factor > my_map["limit_factor"]:
            my_map=rehash(my_map)
        my_map["current_factor"]=curren_factor
        
    return my_map
    

def rehash(my_map):
    numero_a=my_map["capacity"]*2
    si=mf.is_prime(numero_a)
    if not si:
        numero_a=mf.next_prime(numero_a)
    x=new_map(numero_a,my_map["limit_factor"])
    for elemento in my_map["table"]["elements"]:
        if elemento["key"]!=None:
            x=put(x,elemento["key"], elemento["value"])
    return x

def remove(my_map, key):
    for elemento in my_map["table"]["elements"]:
        if elemento["key"]==key:
            elemento["value"]="__EMPTY__"
            elemento["key"]="__EMPTY__"
            my_map["current_factor"] = my_map["size"] / my_map["capacity"]
            my_map["size"]-=1
    return my_map
    
def contains(my_map, key): 
    lista = my_map['table']['elements']
    for llave in lista:
        if me.get_key(llave) == key:
            return True
    return False
    
def size(my_map):
    return my_map['size']


def value_set(my_map):
    cosas=al.new_list()
    for elemento in my_map["table"]["elements"]:
        if elemento["key"]!=None and elemento["key"]!="__EMPTY__":
            cosas=al.add_last(cosas, elemento["value"])
        cosas["size"]=my_map["size"]
    return cosas
    
def new_map(num_elements, load_factor, prime=109345121):
    capacity=mf.next_prime(num_elements/load_factor)
    map={"prime":prime, "capacity":capacity,"scale":1,"shift":0,"table":{"size":capacity,"elements":[]},"current_factor":0,"limit_factor":load_factor,"size":0}
    for i in range(0,capacity):
        
        map["table"]["elements"].append(me.new_map_entry(None, None))
    return map

def get(my_map, key):
    h=mf.hash_value(my_map,key)
    comp, pos=find_slot(my_map,key,h)
    if comp: 
        return my_map["table"]["elements"][pos]["value"]
    else:
        return None    
    
def is_empty(my_map):
    if my_map["size"]==0:
        return True
    return False

def key_set(my_map):
    res = al.new_list()
    for i in my_map["table"]["elements"]:
        if i["key"] is not None and i["key"] != "__EMPTY__":
            al.add_last(res, i["key"])
    return res