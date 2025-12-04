import time
from DataStructures.Map import map_linear_probing as mlp
from DataStructures.Graph import diagraph as G
import csv
from datetime import datetime, timedelta
from math import radians, sin, cos, sqrt, atan2
from DataStructures.List import array_list as al
from DataStructures.List import list_node as ln

def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    return G.new_graph(50000)


# Funciones para la carga de datos

def haversine(lat1, lon1, lat2, lon2):
    """Calcula la distancia Haversine en kilómetros."""
    lat1_rad, lon1_rad = radians(lat1), radians(lon1)
    lat2_rad, lon2_rad = radians(lat2), radians(lon2)
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return 6371 * c



def crear_info_nodo(event_id, lat, lon, timestamp, tag_identifier, comments_m):
    """Crea el diccionario de información (value) de un Punto Migratorio."""
    return {
        'id': event_id,
        'location-lat': lat,
        'location-long': lon,
        'creation-timestamp': timestamp,
        'tag-identifiers': {tag_identifier: True}, 
        'events-count': 1,
        'comments-sum-km': comments_m / 1000.0
    }

def actualizar_info_nodo(info_nodo, tag_identifier, comments_m):
    """Actualiza la información (value) de un nodo existente."""
    info_nodo['tag-identifiers'][tag_identifier] = True 
    info_nodo['events-count'] += 1
    info_nodo['comments-sum-km'] += comments_m / 1000.0
    return info_nodo


# --- Funciones Principales de Carga y Preprocesamiento ---

def load_data(control,filename="1000_cranes_mongolia_small.csv"):
    """
    Carga, limpia y ordena los datos del CSV 
    """
    print(f"Cargando datos desde: {filename}")
    eventos = al.new_list() 
    grullas = al.new_list()
    
    import os
    ruta= os.path.join("Data",filename)
    
    file = open(ruta, 'r', encoding='utf-8')
    
    # 1. Obtener encabezados con readline()
    header_line = file.readline()
    
    # Convertir la línea de encabezado a lista y limpiar
    titulos = [titulos.strip()for titulos in header_line.split(",")]
    
    # 2. Mapeo de índices de columnas
    indices = {}
    i = 0
    while i < len(titulos):
        indices[titulos[i]]=i
        i+= 1
    
    max_index = len(titulos)
    
    # 3. Procesamiento de filas de datos con readline()
    line = file.readline()
    while line:
        
        row = [row.strip() for row in line.split(",")]
        
        event_id = row[indices['event-id']]
        timestamp = datetime.strptime(row[indices['timestamp']],"%Y-%m-%d %H:%M:%S.%f")
        comments_raw = row[indices['comments']]
        comments_raw = comments_raw.replace('"', '').strip()
        comments_m = int(comments_raw)
        tag_identifier = row[indices['tag-local-identifier']]
        lon = float(row[indices['location-long']])
        lat = float(row[indices['location-lat']])

        
        if tag_identifier not in grullas["elements"]:
            grullas=al.add_last(grullas,tag_identifier)
        
        al.add_last(eventos, {
            'event-id': event_id,
            'timestamp': timestamp,
            'location-long': lon,
            'location-lat': lat,
            'comments_m': comments_m,
            'tag-local-identifier': tag_identifier
        })
    
        line = file.readline() # Lectura de la siguiente líneaf
    
    file.close()
    
    # Ordenar los elementos del array_list de eventos
    eventos['elements'].sort(key=lambda x: x['timestamp'])

    print(f"Total de grullas reconocidas: {grullas["size"]}")
    print(f"Total de eventos cargados y procesados: {al.size(eventos)}")
    
    # Contruccion de vertices
    grafo, evento_a_nodo, nodo_keys_creados=reconstruir_vertices(control,eventos)
    grafo_1=reconstruir_arcos(eventos,grullas,grafo,evento_a_nodo,"Distancias Migratorias")
    grafo_2=reconstruir_arcos(eventos,grullas,grafo,evento_a_nodo,"Proximidad de Fuentes Hídricas")

    return grafo_1,grafo_2,nodo_keys_creados

def reconstruir_vertices(control,eventos_al):
    """
    Reconstruye los Vértices/Nodos de Puntos Migratorios.
    
    """
    grafo = control
    evento_a_nodo = mlp.new_map(1,0.5)
    nodo_keys_creados = al.new_list() 
    
    i = 0
    
    size_eventos = al.size(eventos_al)
    while i < size_eventos-1:
        print(i)
        row = al.get_element(eventos_al, i) 
        
        event_id = row['event-id']
        timestamp = row['timestamp']
        lon = row['location-long']
        lat = row['location-lat']
        comments_m = row['comments_m']
        tag_identifier = row['tag-local-identifier']
        
        nodo_encontrado = None
        
        # Iteración en reversa sobre las llaves de los nodos ya creados (array_list)
        j = al.size(nodo_keys_creados) - 1
        nodo_ya_asignado = False 
        
        while j >= 0:
            vertice_id = al.get_element(nodo_keys_creados, j) 
            vertice_completo = G.get_vertex_information(grafo, vertice_id)
            
            if vertice_completo is not None:
                info_nodo = vertice_completo
                
                if not nodo_ya_asignado:
                    dist_haversine = haversine(lat, lon, info_nodo['location-lat'], info_nodo['location-long'])
                    delta_t = timestamp - info_nodo['creation-timestamp']
                    
                    if dist_haversine < 3 and delta_t < timedelta(hours=3):
                        nodo_encontrado = vertice_completo
                        nodo_ya_asignado = True
            
            j = j - 1

        if nodo_encontrado is not None:
            grafo=G.update_vertex_info(grafo,vertice_id,actualizar_info_nodo(nodo_encontrado, tag_identifier, comments_m))
            evento_a_nodo=mlp.put(evento_a_nodo,event_id,vertice_id)
        else:
            info_u = crear_info_nodo(event_id, lat, lon, timestamp, tag_identifier, comments_m)
            G.insert_vertex(grafo, event_id, info_u)
            evento_a_nodo=mlp.put(evento_a_nodo,event_id, event_id)
            al.add_last(nodo_keys_creados, event_id) 

        i = i + 1

    print(f"Total de nodos construidos: {al.size(nodo_keys_creados)}")
    return grafo, evento_a_nodo, nodo_keys_creados

def reconstruir_arcos(eventos_al, grullas, grafo_base, evento_a_nodo, tipo_grafo):
    """
    Calcula los arcos y los inserta en el grafo.
    """
    
    grafo = grafo_base.copy()
    
    arcos_pesos_temporales = {} 

    eventos_por_grulla = mlp.new_map(1,0.5)
    
    # 1. Agrupar eventos por grulla usando array_list para las listas de eventos
    i = 0
    size_eventos = al.size(eventos_al)
    while i < size_eventos-1:
        evento = al.get_element(eventos_al, i)
        tag_id = evento['tag-local-identifier']
        if tag_id not in eventos_por_grulla:
            eventos_por_grulla=mlp.put(eventos_por_grulla,tag_id,al.new_list())
        al.add_last(mlp.get(eventos_por_grulla,tag_id), evento) 
        i = i + 1

    # 2. Iterar sobre cada grulla (lista simple) y crear arcos
    for tag_id in grullas:
        if tag_id in mlp.key_set(eventos_por_grulla)["elements"]:
            eventos_grulla_al = mlp.get(eventos_por_grulla,tag_id)
            nodo_previo_id = None
            
            i = 0
            size_grulla_events = al.size(eventos_grulla_al)
            while i < size_grulla_events:
                row = al.get_element(eventos_grulla_al, i)
                event_id = row['event-id']
                nodo_actual_id = mlp.get(evento_a_nodo,event_id)
                
                if nodo_actual_id is not None:
                    
                    if nodo_previo_id is None:
                        nodo_previo_id = nodo_actual_id
                    else:
                        if nodo_actual_id != nodo_previo_id:
                            nodo_A = G.get_vertex(grafo, nodo_previo_id)['value']
                            nodo_B = G.get_vertex(grafo, nodo_actual_id)['value']
                            
                            peso = 0.0
                            if tipo_grafo == 'Distancias Migratorias':
                                peso = haversine(nodo_A['location-lat'], nodo_A['location-long'], 
                                                 nodo_B['location-lat'], nodo_B['location-long'])
                            elif tipo_grafo == 'Proximidad de Fuentes Hídricas':
                                peso = nodo_B['comments-sum-km'] / nodo_B['events-count']

                            key = (nodo_previo_id, nodo_actual_id)
                            if key not in arcos_pesos_temporales:
                                arcos_pesos_temporales[key] = []
                            arcos_pesos_temporales[key].append(peso)
                            
                            nodo_previo_id = nodo_actual_id
                
                i = i + 1

    # 3. Insertar arcos promediados
    total_arcos_finales = 0
    for key  in arcos_pesos_temporales:
        pesos=arcos_pesos_temporales["key"]
        promedio_peso = sum(pesos) / len(pesos)
        G.add_edge(grafo, key[0], key[1], promedio_peso)
        total_arcos_finales = total_arcos_finales + 1
    
    grafo['num_edges'] = total_arcos_finales 

    print(f"Total de arcos construidos para {tipo_grafo}: {total_arcos_finales}")
    
    return grafo




def req1(graph_migratory, lat_origen_user, lon_origen_user, lat_destino_user, lon_destino_user, grulla_id):
    origen_key, destino_key = None, None
    min_dist_origen, min_dist_destino = float('inf'), float('inf')
    
    all_keys_list = G.get_vertices(graph_migratory)
    
    current_key_node = al.first_element(all_keys_list)
    while current_key_node is not None:
        node_key = ln.get_element(current_key_node)
        
        info = G.get_vertex_information(graph_migratory, node_key)
        lat, lon = info['location-lat'], info['location-long']
        
        dist_o = haversine(lat_origen_user, lon_origen_user, lat, lon) 
        if dist_o < min_dist_origen:
            min_dist_origen = dist_o
            origen_key = node_key
            
        dist_d = haversine(lat_destino_user, lon_destino_user, lat, lon)
        if dist_d < min_dist_destino:
            min_dist_destino = dist_d
            destino_key = node_key
            
        current_key_node = ln.get_next(current_key_node)

    if origen_key is None or destino_key is None:
        return "ERROR: No se pudieron encontrar puntos migratorios cercanos para el origen o el destino."

    origen_info = G.get_vertex_information(graph_migratory, origen_key)
    grullas_en_origen_al = origen_info.get('tag-identifiers', al.new_list()) 
        
    if not al_contains(grullas_en_origen_al, grulla_id):
        return (f"No se puede iniciar la ruta. La grulla con ID '{grulla_id}' "
                f"no pasó por el nodo de origen más cercano ({origen_key}).")

    visited = mlp.new_map() 
    path = al.new_list()
    
    camino_encontrado = buscar_camino_dfs(
        graph_migratory, 
        origen_key, 
        destino_key, 
        visited, 
        path
    )
    
    if camino_encontrado is None:
        return "No se reconoció un camino viable entre los puntos migratorios especificados."

    total_distancia_desplazamiento = 0.0
    nodos_en_ruta = camino_encontrado 
    total_puntos = al.size(nodos_en_ruta)

    for i in range(total_puntos - 1):
        u = al_get_element_by_index_safe(nodos_en_ruta, i)
        v = al_get_element_by_index_safe(nodos_en_ruta, i+1)
        
        distancia_arco = get_arc_weight(graph_migratory, u, v) 
        total_distancia_desplazamiento += distancia_arco

    puntos_a_mostrar = []
    
    indices_set = set(range(min(5, total_puntos)))
    indices_set.update(range(max(0, total_puntos - 5), total_puntos))
    indices_list = sorted(list(indices_set))

    for i in indices_list:
        node_key = al_get_element_by_index_safe(nodos_en_ruta, i)
        node_info = G.get_vertex_information(graph_migratory, node_key)
        
        if i < total_puntos - 1:
            next_key = al_get_element_by_index_safe(nodos_en_ruta, i+1)
            dist_al_sig = get_arc_weight(graph_migratory, node_key, next_key)
            if dist_al_sig == 0.0: dist_al_sig = "Desconocido"
            else: dist_al_sig = f"{dist_al_sig:.4f}"
        else:
            dist_al_sig = "Fin de Ruta"
            
        grullas_list_al = node_info.get('tag-identifiers', al.new_list())
        total_grullas = al.size(grullas_list_al)
        
        muestra_grullas = []
        if total_grullas > 0:
            for j in range(min(3, total_grullas)):
                muestra_grullas.append(al_get_element_by_index_safe(grullas_list_al, j))
            
            if total_grullas > 6:
                muestra_grullas.append("...")
            
            if total_grullas > 3:
                start_index = max(3, total_grullas - 3) if total_grullas > 6 else 3
                for j in range(start_index, total_grullas):
                    muestra_grullas.append(al_get_element_by_index_safe(grullas_list_al, j))
        
        grullas_muestra_str = f"[{', '.join(map(str, muestra_grullas))}]"
        if total_grullas == 0: grullas_muestra_str = "Desconocido"

        puntos_a_mostrar.append({
            'Identificador': node_key,
            'Latitud': node_info.get('location-lat', 'Unknown'),
            'Longitud': node_info.get('location-long', 'Unknown'),
            'No. Individuos': total_grullas,
            'Grullas (Muestra)': grullas_muestra_str,
            'Desplazamiento al siguiente (km)': dist_al_sig
        })
        
    primer_nodo_con_individuo = origen_key 
    
    respuesta = f"## 🗺️ Camino Migratorio Encontrado (Grulla ID: {grulla_id})"
    respuesta += f"\n\n**✅ Mensaje:** La ruta se inicia en el nodo **{primer_nodo_con_individuo}** (el más cercano al origen y donde el individuo está presente)."
    respuesta += f"\n\n- **Distancia de Desplazamiento Total:** {total_distancia_desplazamiento:.4f} Km"
    respuesta += f"\n- **Total de Puntos (Nodos) en el Camino:** {total_puntos}"
    respuesta += f"\n- **Punto de Origen (GPS más cercano):** {origen_key} (Distancia de aproximación: {min_dist_origen:.4f} Km)"
    respuesta += f"\n- **Punto de Destino (GPS más cercano):** {destino_key} (Distancia de aproximación: {min_dist_destino:.4f} Km)"
    respuesta += "\n\n### Muestra de Vértices en la Ruta"
    
    tabla = "| Identificador | Latitud | Longitud | Grullas (Total) | Muestra de Grullas | Desplazamiento al Siguiente (km) |\n"
    tabla += "| :--- | :--- | :--- | :--- | :--- | :--- |\n"
    
    for punto in puntos_a_mostrar:
        tabla += f"| {punto['Identificador']} | {punto['Latitud']} | {punto['Longitud']} | {punto['No. Individuos']} | {punto['Grullas (Muestra)']} | {punto['Desplazamiento al siguiente (km)']} |\n"

    respuesta += "\n" + tabla
    
    return respuesta

def al_contains(al_list, element):
    current_node = al.first_element(al_list)
    
    while current_node is not None:
        if ln.get_element(current_node) == element:
            return True
        current_node = ln.get_next(current_node)
        
    return False

def al_get_element_by_index_safe(al_list, index):
    current_node = al.first_element(al_list)
    count = 0
    
    while current_node is not None:
        if count == index:
            return ln.get_element(current_node)
        current_node = ln.get_next(current_node)
        count += 1
    return None

def get_arc_weight(graph, u_key, v_key):
    info_nodo_u = G.get_vertex_information(graph, u_key)
    vecinos_u = info_nodo_u.get('adjacents', al.new_list())
    
    current_node = al.first_element(vecinos_u)
    
    while current_node is not None:
        arco_tuple = ln.get_element(current_node)
        vecino_key = arco_tuple[0]
        peso_arco = arco_tuple[1]
        
        if vecino_key == v_key:
            return peso_arco
        
        current_node = ln.get_next(current_node)
        
    return 0.0

def buscar_camino_dfs(grafo, origen_key, destino_key, visited, camino_actual):
    
    if mlp.get_element(visited, origen_key) is not None: 
        return None 
    
    mlp.insert_element(visited, origen_key, True) 
    al.add_last(camino_actual, origen_key)

    if origen_key == destino_key:
        return al.copy(camino_actual) 

    info_nodo = G.get_vertex_information(grafo, origen_key)
    vecinos = info_nodo.get('adjacents', al.new_list()) 

    current_node = al.first_element(vecinos)
    while current_node is not None: 
        vecino_tuple = ln.get_element(current_node)
        vecino_key = vecino_tuple[0] 
        
        camino_encontrado = buscar_camino_dfs(
            grafo, 
            vecino_key, 
            destino_key, 
            visited, 
            camino_actual
        )
        
        if camino_encontrado is not None:
            return camino_encontrado
        
        current_node = ln.get_next(current_node)
    
    al.remove_last(camino_actual)
    return None


def req2(catalog):
    pass


def req_3(catalog):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


def req4(graph_migratory, lat_origen_user, lon_origen_user):
    origen_key = None
    min_dist_origen = float('inf')
    
    
    all_keys_list = G.get_vertices(graph_migratory)
    
    list_size = al.size(all_keys_list)
    for i in range(list_size):
        node_key = al_get_element_by_index_safe(all_keys_list, i)
        
        info = G.get_vertex_information(graph_migratory, node_key)
        lat, lon = info['location-lat'], info['location-long']
        
        dist_o = haversine(lat_origen_user, lon_origen_user, lat, lon) 
        if dist_o < min_dist_origen:
            min_dist_origen = dist_o
            origen_key = node_key

    if origen_key is None:
        return "ERROR: No se pudo encontrar un punto migratorio cercano al origen."

    
    resultado_prim = correr_prim(graph_migratory, origen_key)

    if resultado_prim is None:
        return "No se reconoció una red hídrica viable a partir del origen especificado."

    total_distancia_hídrica, corridor_nodes_list = resultado_prim
    
    
    total_puntos = al.size(corridor_nodes_list)
    total_individuals = 0
    
    list_size = al.size(corridor_nodes_list)
    for i in range(list_size):
        node_key = al_get_element_by_index_safe(corridor_nodes_list, i)
        info = G.get_vertex_information(graph_migratory, node_key)
        grullas_list_al = info.get('tag-identifiers', al.new_list())
        total_individuals += al.size(grullas_list_al)

    puntos_a_mostrar = []
    
  
    indices_set = set(range(min(5, total_puntos)))
    indices_set.update(range(max(0, total_puntos - 5), total_puntos))
    indices_list = sorted(list(indices_set))

    for i in indices_list:
        node_key = al_get_element_by_index_safe(corridor_nodes_list, i)
        node_info = G.get_vertex_information(graph_migratory, node_key)
            
        grullas_list_al = node_info.get('tag-identifiers', al.new_list())
        total_grullas = al.size(grullas_list_al)
        
        muestra_grullas = []
        if total_grullas > 0:
            for j in range(min(3, total_grullas)):
                muestra_grullas.append(al_get_element_by_index_safe(grullas_list_al, j))
            
            if total_grullas > 6:
                muestra_grullas.append("...")
            
            if total_grullas > 3:
                start_index = max(3, total_grullas - 3) if total_grullas > 6 else 3
                for j in range(start_index, total_grullas):
                    muestra_grullas.append(al_get_element_by_index_safe(grullas_list_al, j))
        
        grullas_muestra_str = f"[{', '.join(map(str, muestra_grullas))}]"
        if total_grullas == 0: grullas_muestra_str = "Desconocido"

        puntos_a_mostrar.append({
            'Identificador': node_key,
            'Latitud': node_info.get('location-lat', 'Unknown'),
            'Longitud': node_info.get('location-long', 'Unknown'),
            'No. Individuos': total_grullas,
            'Grullas (Muestra)': grullas_muestra_str
        })
        
    respuesta = f"## Estimación de Corredores Hídricos Óptimos (Algoritmo de Prim)"
    respuesta += f"\n\n- **Total de Puntos en el Corredor:** {total_puntos}"
    respuesta += f"\n- **Total de Individuos Utilizando la Red:** {total_individuals}"
    respuesta += f"\n- **Distancia Total a Fuentes Hídricas (Corredor MST):** {total_distancia_hídrica:.4f} Km"
    respuesta += f"\n- **Punto de Origen (GPS más cercano):** {origen_key} (Distancia de aproximación: {min_dist_origen:.4f} Km)"
    respuesta += "\n\n### Muestra de Vértices en el Corredor Migratorio (Orden BFS)"
    
    tabla = "| Identificador | Latitud | Longitud | Grullas (Total) | Muestra de Grullas |\n"
    tabla += "| :--- | :--- | :--- | :--- | :--- |\n"
    
    for punto in puntos_a_mostrar:
        tabla += f"| {punto['Identificador']} | {punto['Latitud']} | {punto['Longitud']} | {punto['No. Individuos']} | {punto['Grullas (Muestra)']} |\n"

    respuesta += "\n" + tabla
    
    return respuesta


def al_contains(al_list, element):
    list_size = al.size(al_list)
    found = False
    i = 0
    while i < list_size and found == False:
        if al_get_element_by_index_safe(al_list, i) == element:
            found = True
        i += 1
    return found

def al_get_element_by_index_safe(al_list, index):
   
    current_node = al_list.first_node 
    count = 0
    result = None
    
    while current_node is not None and result is None:
        if count == index:
            result = ln.get_element(current_node)
        
        if result is None:
            current_node = ln.get_next(current_node)
            count += 1
            
    return result

def get_arc_weight(graph, u_key, v_key):
    info_nodo_u = G.get_vertex_information(graph, u_key)
    vecinos_u = info_nodo_u.get('adjacents', al.new_list())
    
    list_size = al.size(vecinos_u)
    result = 0.0
    
    for i in range(list_size):
        arco_tuple = al_get_element_by_index_safe(vecinos_u, i)
        vecino_key = arco_tuple[0]
        peso_arco = arco_tuple[1]
        
        if vecino_key == v_key:
            result = peso_arco
        
    return result

def correr_prim(grafo, origen_key):
    
    all_keys_list = G.get_vertices(grafo)
    
    min_weight = mlp.new_map()
    parent = mlp.new_map()
    in_mst = mlp.new_map()
    
    pq = pq.new_pq()
    
    list_size = al.size(all_keys_list)
    for i in range(list_size):
        key = al_get_element_by_index_safe(all_keys_list, i)
        
        mlp.insert_element(min_weight, key, float('inf'))
        mlp.insert_element(parent, key, None)
        mlp.insert_element(in_mst, key, False)
        
        initial_priority = float('inf')
        if key == origen_key:
            initial_priority = 0
            
        pq.insert_element(pq, initial_priority, key) 

    total_mst_distance = 0.0
    mst_nodes_count = 0
    
    mst_adj = mlp.new_map()

    while not pq.is_empty(pq):
        
        result_tuple = pq.extract_min(pq)
        weight_to_u = result_tuple[0]
        u = result_tuple[1]
        
       
        if mlp.get_element(in_mst, u) == False or mlp.get_element(in_mst, u) is None:
            
            mlp.insert_element(in_mst, u, True)
            mst_nodes_count += 1
            
            u_parent = mlp.get_element(parent, u)
            if u_parent is not None:
                total_mst_distance += weight_to_u
                
                u_adj = mlp.get_element(mst_adj, u_parent)
                if u_adj is None:
                    u_adj = al.new_list()
                    mlp.insert_element(mst_adj, u_parent, u_adj)
                al.add_last(u_adj, u)

            u_info = G.get_vertex_information(grafo, u)
            vecinos = u_info.get('adjacents', al.new_list()) 
            
            list_size = al.size(vecinos)
            for i in range(list_size):
                vecino_tuple = al_get_element_by_index_safe(vecinos, i)
                v = vecino_tuple[0] 
                peso_arco = vecino_tuple[1] 
                
                if mlp.get_element(in_mst, v) == False or mlp.get_element(in_mst, v) is None:
                    current_min_v = mlp.get_element(min_weight, v)
                    
                    if peso_arco < current_min_v:
                        
                        mlp.insert_element(min_weight, v, peso_arco)
                        mlp.insert_element(parent, v, u)
                        
                        pq.improve_priority(pq, peso_arco, v)

    if mst_nodes_count == 0:
        return None

   
    corridor_nodes_list = al.new_list()
    queue = al.new_list()
    visited_bfs = mlp.new_map()
    
    al.add_last(queue, origen_key)
    mlp.insert_element(visited_bfs, origen_key, True)
    
    while al.size(queue) > 0:
        u = al_get_element_by_index_safe(queue, 0)
        al.remove_first(queue)
        
        al.add_last(corridor_nodes_list, u)
        
        u_children = mlp.get_element(mst_adj, u)
        
        if u_children is not None:
            list_size = al.size(u_children)
            for i in range(list_size):
                v = al_get_element_by_index_safe(u_children, i)
                if mlp.get_element(visited_bfs, v) is None:
                    mlp.insert_element(visited_bfs, v, True)
                    al.add_last(queue, v)
                
    return total_mst_distance, corridor_nodes_list

def buscar_camino_bfs(grafo, origen_key, destino_key):
    queue = al.new_list()
    visited = mlp.new_map()
    predecessor = mlp.new_map()

    al.add_last(queue, origen_key)
    mlp.insert_element(visited, origen_key, True) 
    
    found = False
    
    # Reemplazo de 'break' por una condición en el while
    while al.size(queue) > 0 and found == False:
        
        u = al_get_element_by_index_safe(queue, 0)
        al.remove_first(queue)

        if u == destino_key:
            found = True
        
        # Solo procesar vecinos si aún no se ha encontrado el destino
        if found == False:
            info_nodo_u = G.get_vertex_information(grafo, u)
            vecinos = info_nodo_u.get('adjacents', al.new_list()) 
            
            list_size = al.size(vecinos)
            for i in range(list_size):
                vecino_tuple = al_get_element_by_index_safe(vecinos, i)
                v = vecino_tuple[0] 
                
                if mlp.get_element(visited, v) is None:
                    mlp.insert_element(visited, v, True)
                    mlp.insert_element(predecessor, v, u)
                    al.add_last(queue, v)

    if found == False:
        return None
    
    path_al = al.new_list()
    current = destino_key
    
    reconstruction_finished = False
    # Reemplazo del 'break' por una condición en el while
    while current is not None and reconstruction_finished == False:
        al.add_first(path_al, current) 
        
        if current == origen_key:
            reconstruction_finished = True
        
        if reconstruction_finished == False:
            current = mlp.get_element(predecessor, current)
        
    if al.size(path_al) > 0 and al_get_element_by_index_safe(path_al, 0) == origen_key:
        return path_al
    else:
        return None


def req_5(catalog):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(catalog):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed

