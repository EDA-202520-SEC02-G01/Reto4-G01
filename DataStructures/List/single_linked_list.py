def new_list():
    newlist={"first": None, "last": None, "size": 0}
    return newlist

def get_element(my_list, pos):
    searchpos=0
    node=my_list["first"]
    while searchpos<pos:
        node=node["next"]
        searchpos+=1
    return node['info']

def is_present(my_list, element, cmp_function):
    is_in_array=False
    temp=my_list["first"]
    count=0
    while not is_in_array and temp is not None:
        if cmp_function(element, temp["info"])==0:
            is_in_array=True
        else:
            temp=temp["next"]
            count+=1
    if not is_in_array:
        count=-1
    return count

def add_first(my_list, elemento):
    nodo={"info":elemento, "next":None}
    my_list["size"]+=1
    if my_list["first"]==None:
        my_list["first"]=nodo
        my_list["last"]=nodo
    else:
        nodo["next"]=my_list["first"]
        my_list["first"]=nodo
        
def add_last(my_list, elemento):
    nodo={"info":elemento, "next":None}
    my_list["size"]+=1
    if my_list["first"]==None:
        my_list["first"]=nodo
        my_list["last"]=nodo
    else:
        my_list["last"]["next"]=nodo
        my_list["last"]=nodo
        
def size(my_list):
    return my_list["size"]

def first_element(my_list):
    if not my_list["first"]==None:
        return my_list["first"]["info"]
    else:
        raise IndexError("list index out of range")

def is_empty(my_list):
    res=False
    if my_list["size"] == 0:
        res=True
    return res

def last_element(my_list):
    if not my_list["last"]==None:
        return my_list["last"]["info"]
    else:
        raise Exception('IndexError: list index out of range')

def delete_element(my_list, pos):
    if pos<0 or pos>=my_list["size"]:
        raise Exception('IndexError: list index out of range')
    my_list["size"]-=1
    if pos==0:
        nodo=my_list["first"]["next"]
        my_list["first"]=nodo   
        if my_list["size"]==0:
            my_list["last"]=nodo 
    else:
        contador=0
        nodo=my_list["first"]
        while contador!=pos-1:
            nodo=nodo["next"]
            contador+=1
        if pos==my_list["size"]-2:
            nodo["next"]=None
            my_list["last"]=nodo 
        eliminar=nodo["next"]
        salta=eliminar["next"]
        nodo["next"]=salta 
    return my_list
          
def remove_first(my_list):
    if my_list["size"]==0:
       raise Exception('IndexError: list index out of range') 
    elif my_list["size"]==1:
        valor=my_list["first"]["info"]
        my_list["first"] = None
        my_list["last"] = None
        my_list["size"]-=1
    elif my_list["size"]!=0:
        valor=my_list["first"]["info"]
        my_list["size"]-=1
        nodo=my_list["first"]["next"]
        my_list["first"]=nodo   
    return valor
    
def remove_last(my_list):
    if my_list["size"]==0:
       raise Exception('IndexError: list index out of range') 
    elif my_list["size"]==1:
        valor=my_list["last"]["info"]
        my_list["first"] = None
        my_list["last"] = None
        my_list["size"]-=1
    elif my_list["size"]!=0:
        valor=my_list["last"]["info"]
        my_list["size"]-=1
        contador=0
        nodo=my_list["first"]
        while contador!=my_list["size"]-2:
            nodo=nodo["next"]
            contador+=1
        nodo["next"]=None
        my_list["last"]=nodo 
    return valor
    
def insert_element(my_list, element, pos):
    if pos<0 or pos>my_list["size"]:
        raise Exception('IndexError: list index out of range')
    my_list["size"]+=1
    nuevo={"info":element, "next":None}
    if pos==0:
        nuevo["next"]=my_list["first"]
        my_list["first"]=nuevo   
        if my_list["size"]==1:
            my_list["last"]=nuevo 
    else:
        contador=0
        nodo=my_list["first"]
        while contador!=pos-1:
            nodo=nodo["next"]
            contador+=1
        if pos==my_list["size"]-1:
            nodo["next"]=nuevo
            my_list["last"]=nuevo 
        siguiente=nodo["next"]
        nuevo["next"]=siguiente
        nodo["next"]=nuevo
    return my_list
    
def change_info(my_list, pos, new_info):
    if pos<0 or pos>=my_list["size"]:
        raise Exception('IndexError: list index out of range')
    contador=0
    nodo=my_list["first"]
    while contador!=pos:
        nodo=nodo["next"]
        contador+=1
    nodo["info"]=new_info
    return my_list
      
def exchange(my_list, pos_1, pos_2):
    if ( pos_1<0 or pos_1>=my_list["size"]) or ( pos_2<0 or pos_2>=my_list["size"]):
        raise Exception('IndexError: list index out of range')
    contador=0
    nodo=my_list["first"]
    while contador!=my_list["size"]:
        if contador==pos_1:
            nodo1=nodo
            info1=nodo["info"]
        if contador==pos_2:
            nodo2=nodo
            info2=nodo["info"]
        nodo=nodo["next"]
        contador+=1
    nodo1["info"]=info2
    nodo2["info"]=info1
    return my_list
    
def sub_list(my_list, pos_i, num_elements):
    if pos_i<0 or pos_i>=my_list["size"]:
        raise Exception('IndexError: list index out of range')
    if num_elements == 0:
        return {"first": None, "last": None, "size": 0}
    newlist={"first": None, "last": None, "size": 0}
    contador=0
    nodo=my_list["first"]
    while nodo!=None and contador<pos_i+num_elements:
        if contador==pos_i:
            nodo_c={"info":nodo["info"], "next":None}
            newlist["first"]=nodo_c
            newlist["size"]+=1
        elif contador>pos_i:
            nodo_c={"info":nodo["info"], "next":None}
            anterior["next"]=nodo_c
            newlist["size"]+=1
        anterior=nodo_c
        contador+=1
    newlist["last"]=anterior
    nodo_c["next"]=None
    return newlist

def sub_lista(my_list, pos_i, num_elements):

    if pos_i < 0 or pos_i >= my_list["size"]:
        raise Exception('IndexError: list index out of range')

    if num_elements == 0:
        return {"first": None, "last": None, "size": 0}

    newlist = {"first": None, "last": None, "size": 0}
    contador = 0
    nodo = my_list["first"]

    anterior = None
    nodo_c = None
    fin = pos_i + num_elements

    while nodo is not None and contador < fin:
        if contador == pos_i:
           
            nodo_c = {"info": nodo["info"], "next": None}
            newlist["first"] = nodo_c
            newlist["size"] += 1
            anterior = nodo_c
        elif contador > pos_i:
            
            nodo_c = {"info": nodo["info"], "next": None}
            anterior["next"] = nodo_c
            newlist["size"] += 1
            anterior = nodo_c
      
        nodo = nodo["next"]
        contador += 1

    if newlist["size"] == 0:
        return {"first": None, "last": None, "size": 0}

    newlist["last"] = anterior
    if newlist["last"] is not None:
        newlist["last"]["next"] = None

    return newlist
