from DataStructures.Map import map_linear_probing as mlp
from DataStructures.Graph import diagraph as G
from DataStructures.Queue import queue as q
from DataStructures.Stack import stack as st

def bfs(graph, source):
    visited_ht = map.new_map(num_elements=G.order(graph), load_factor=0.5)
    bfs_vertex(graph, source, visited_ht)
    return visited_ht

def bfs_vertex(my_graph, source, visited_ht):
    queue = q.new_queue()
    q.enqueue(queue, source)

    visited_ht[source]["marked"] = True
    visited_ht[source]["edge_from"] = None
    visited_ht[source]["dist_to"] = 0

    while not q.is_empty(queue):
        vertex = q.dequeue(queue)
        adj = G.edges_vertex(my_graph, vertex)

        for edge in adj:
            w = edge["vertex"]

            if not mlp.contains(visited_ht, w):
                mlp.put(visited_ht, w, {
                    "marked": True,
                    "edge_from": vertex,
                    "dist_to": visited_ht[vertex]["dist_to"] + 1
                })

                q.enqueue(queue, w)

    return visited_ht


def has_path_to(vertex, structure):
    visited = structure["visited"]

    if mlp.contains(visited, vertex):
        info = mlp.get(visited, vertex)
        if info["marked"] is True:
            return True

    return False

def path_to(vertex, visited_ht):
    
    if vertex not in visited_ht["marked"]:
        return None

    path = st.new_stack()

    while vertex is not None:
        st.push(path, vertex)
        vertex = visited_ht["edge_to"].get(vertex, None)

    return path
