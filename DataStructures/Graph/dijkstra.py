from DataStructures.Map import map_linear_probing as mlp
from DataStructures.Graph import diagraph as G
from DataStructures.Queue import queue as pq
from DataStructures.Graph import dijsktra_structure as dijkstra_structure
from DataStructures.Graph import dijsktra_structure 
from DataStructures.Stack import stack as st
from DataStructures.Graph import vertex as v

import math

def init_structure(graph, source):
    structure = dijsktra_structure.new_dijsktra_structure(source, G.order(graph))
    vertices = G.vertices(graph)
    for i in range(lt.size(vertices)):
        vert = lt.get_element(vertices, i)
        map.put(structure["visited"], vert, {"marked":False, "edge_from":None,"dist_to":math.inf})
    map.put(structure["visited"], source, {"marked":False, "edge_from":None, "dist_to":0})
    pq.insert(structure["pq"], source, 0 )
    return structure

def has_path_to(vertex, structure):
    visited = structure["visited"]

    if mlp.contains(visited, vertex):
        info = mlp.get(visited, vertex)
        if info["marked"] is True:
            return True

    return False

def path_to(visited,key_v):

    info = map.get(visited, key_v)
    if info is None:
        return None

    info = info["value"]

    if info["dist_to"] == math.inf:
        return None

    stack = st.new_stack()

    v = key_v
    while v is not None:
        st.push(stack, v)
        v = mlp.get(visited, v)["value"]["edge_from"]

    return stack

