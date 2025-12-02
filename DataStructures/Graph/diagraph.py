from DataStructures.Map import map_linear_probing as mp
from DataStructures.Graph import vertex as vtx
from DataStructures.Graph import edge as edg
from DataStructures.List import array_list as al
from DataStructures.Map import map_functions as mf

def add_edge(my_graph, key_u, key_v, weight=1.0):

    vertex_u = mp.get(my_graph["vertices"], key_u)
    if vertex_u is None:
        raise Exception("El vertice u no existe")

    vertex_v = mp.get(my_graph["vertices"], key_v)
    if vertex_v is None:
        raise Exception("El vertice v no existe")

    adj_u = vtx.get_adjacents(vertex_u)

    existing_edge = mp.get(adj_u, key_v)

    if existing_edge is not None:
        edg.set_weight(existing_edge, weight)
        mp.put(adj_u, key_v, existing_edge)
    else:
        new_e = edg.new_edge(key_v, weight)
        mp.put(adj_u, key_v, new_e)
        my_graph["num_edges"] += 1

    return my_graph


def size(my_graph):
    return my_graph["num_edges"]


def degree(my_graph, key_u):
    vertex_u = mp.get(my_graph["vertices"], key_u)
    if vertex_u is None:
        raise Exception("El vertice no existe")

    return vtx.degree(vertex_u)

def edges_vertex(my_graph, key_u):

    vertex_u = mp.get(my_graph["vertices"], key_u)
    if vertex_u is None:
        raise Exception("El vertice no existe")

    adj = vtx.get_adjacents(vertex_u)

    result = al.new_list()

    keys = mp.key_set(adj)
    for key_v in keys:
        edge = mp.get(adj, key_v)
        al.add_last(result, edge)

    return result

def get_vertex_information(my_graph, key_u):

    vertex_u = mp.get(my_graph["vertices"], key_u)
    if vertex_u is None:
        raise Exception("El vertice no existe")

    return vtx.get_value(vertex_u)

def new_graph(order):
    vertices=mp.new_map(order,0.5)
    return vertices

def contains_vertex(my_graph, key_u):
    res=mp.contains(my_graph,key_u)
    return res

def adjacents(my_graph, key_u):
    vertex=mp.get(my_graph, key_u)
    adj=vtx.get_adjacents(vertex)
    if mp.is_empty(adj) == False and vertex != None:
        return mp.key_set(adj)
    elif vertex != None and mp.is_empty(adj) == True:
        return []
    else:
        return "el vertice no existe"
    
    
    



    


def insert_vertex(my_graph, key_u, info_u):
    vertex=vtx.new_vertex(key_u,info_u)
    mp.put(my_graph["vertices"],key_u,vertex)
    return my_graph

def order(my_graph):
    cantidad=mp.size(my_graph)
    return cantidad

def vertices(my_graph):
    return mp.key_set(my_graph)

def update_vertex_info(my_graph, key_u, new_info_u):
    my_map=my_graph["vertices"]
    valor=mf.hash_value(my_map,key_u)
    estado,pos=mp.find_slot(my_map,key_u,valor)
    if estado:
        my_map["table"]["elements"][pos]["value"]=new_info_u
    return my_graph

