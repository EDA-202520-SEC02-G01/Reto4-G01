import time
from DataStructures.Map import map_linear_probing as mlp
from DataStructures.Graph import diagraph as G
import csv
from datetime import datetime, timedelta
from math import radians, sin, cos, sqrt, atan2
from DataStructures.List import array_list as al

def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    return G.new_graph(1)


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

def load_data(control,filename="1000_cranes_mongolia_large.csv"):
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
        comments_m = int(row[indices['comments']])
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

    return grafo_1,grafo_2,eventos,nodo_keys_creados

def reconstruir_vertices(control,eventos_al):
    """
    Reconstruye los Vértices/Nodos de Puntos Migratorios.
    
    """
    grafo = control
    evento_a_nodo = mlp.new_map(1,0.5)
    nodo_keys_creados = al.new_list() 
    
    i = 0
    size_eventos = al.size(eventos_al)
    while i < size_eventos:
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
            grafo=G.update_vertex_info(grafo,nodo_encontrado["key"],actualizar_info_nodo(nodo_encontrado['value'], tag_identifier, comments_m))
            evento_a_nodo=mlp.put(evento_a_nodo,event_id,nodo_encontrado['key'])
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
    Utiliza G.new_graph, G.get_vertex, G.add_edge y funciones al.
    """
    
    grafo = grafo_base.copy()
    
    arcos_pesos_temporales = {} 

    eventos_por_grulla = mlp.new_map(1,0.5)
    
    # 1. Agrupar eventos por grulla usando array_list para las listas de eventos
    i = 0
    size_eventos = al.size(eventos_al)
    while i < size_eventos:
        evento = al.get_element(eventos_al, i)
        tag_id = evento['tag-local-identifier']
        if tag_id not in eventos_por_grulla:
            eventos_por_grulla=mlp.put(eventos_por_grulla,tag_id,al.new_list())
        al.add_last(eventos_por_grulla[tag_id], evento) 
        i = i + 1

    # 2. Iterar sobre cada grulla (lista simple) y crear arcos
    for tag_id in grullas:
        if tag_id in eventos_por_grulla:
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




def req_1(catalog):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    pass


def req_2(catalog):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(catalog):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


def req_4(catalog):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    pass


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

