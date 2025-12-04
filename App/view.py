import sys
from App import logic as lo
from DataStructures.List import array_list as al
from DataStructures.Graph import diagraph as G

def new_logic():
    """
        Se crea una instancia del controlador
    """
    return lo.new_logic()

def print_menu():
    print("Bienvenido")
    print("0- Cargar información")
    print("1- Ejecutar Requerimiento 1")
    print("2- Ejecutar Requerimiento 2")
    print("3- Ejecutar Requerimiento 3")
    print("4- Ejecutar Requerimiento 4")
    print("5- Ejecutar Requerimiento 5")
    print("6- Ejecutar Requerimiento 6")
    print("7- Salir")

def load_data(control):
    """
    Carga los datos
    """
    filename=input("Introduce el nombre del archivo: ")
    if filename=="":
        grafo1,grafo2, nodo_keys_creados_al=lo.load_data(control)
    else:
        grafo1,grafo2, nodo_keys_creados_al=lo.load_data(control,filename)
    
    print("\nGrafo de Distancias Migratorias")
    print("\nPrimeros 5 Nodos Creados")
    size_nodos = al.size(nodo_keys_creados_al)
    max_a_mostrar = 5
    i = 0
    while i < size_nodos:
        if i < max_a_mostrar:
            vertice_key = al.get_element(nodo_keys_creados_al, i) # Uso correcto de al.get_element
            data = imprimir_info_nodo(grafo1,vertice_key)
            print(f"  - ID: {data['id']}")
            print(f"    - Posición (Lat, Lon): ({data['posicion'][0]:.6f}, {data['posicion'][1]:.6f})")
            print(f"    - Fecha de Creación: {data['creacion']}")
            print(f"    - Identificadores de Grullas: {data['grullas_id']}")
            print(f"    - Conteo de Eventos: {data['eventos_count']}")
        i = i + 1
        
    print("\nÚltimos 5 Nodos Creados")
    inicio_ultimos = max(0, size_nodos - 5)
    i = inicio_ultimos
    while i < size_nodos: 
        vertice_key = al.get_element(nodo_keys_creados_al, i) 
        data = imprimir_info_nodo(grafo1,vertice_key)
        print(f"  - ID: {data['id']}")
        print(f"    - Posición (Lat, Lon): ({data['posicion'][0]:.6f}, {data['posicion'][1]:.6f})")
        print(f"    - Fecha de Creación: {data['creacion']}")
        print(f"    - Identificadores de Grullas: {data['grullas_id']}")
        print(f"    - Conteo de Eventos: {data['eventos_count']}")
        i = i + 1
        
    print("\n")
    print("\nGrafo de Proximidad de Fuentes Hídricas")
    print("\nPrimeros 5 Nodos Creados")
    size_nodos = al.size(nodo_keys_creados_al)
    max_a_mostrar = 5
    i = 0
    while i < size_nodos:
        if i < max_a_mostrar:
            vertice_key = al.get_element(nodo_keys_creados_al, i) # Uso correcto de al.get_element
            data = imprimir_info_nodo(grafo2,vertice_key)
            print(f"  - ID: {data['id']}")
            print(f"    - Posición (Lat, Lon): ({data['posicion'][0]:.6f}, {data['posicion'][1]:.6f})")
            print(f"    - Fecha de Creación: {data['creacion']}")
            print(f"    - Identificadores de Grullas: {data['grullas_id']}")
            print(f"    - Conteo de Eventos: {data['eventos_count']}")
        i = i + 1
        
    print("\nÚltimos 5 Nodos Creados")
    inicio_ultimos = max(0, size_nodos - 5)
    i = inicio_ultimos
    while i < size_nodos: 
        vertice_key = al.get_element(nodo_keys_creados_al, i) 
        data = imprimir_info_nodo(grafo2,vertice_key)
        print(f"  - ID: {data['id']}")
        print(f"    - Posición (Lat, Lon): ({data['posicion'][0]:.6f}, {data['posicion'][1]:.6f})")
        print(f"    - Fecha de Creación: {data['creacion']}")
        print(f"    - Identificadores de Grullas: {data['grullas_id']}")
        print(f"    - Conteo de Eventos: {data['eventos_count']}")
        i = i + 1
    
def imprimir_info_nodo(grafo,vertice_key):
        """Función auxiliar para formatear la información del nodo."""
        vertice = G.get_vertex_information(grafo, vertice_key)
        info = vertice
        grullas_id = []
        for tag_id in info['tag-identifiers']: 
            grullas_id.append(tag_id)
        
        return {
            'id': info['id'],
            'posicion': (info['location-lat'], info['location-long']),
            'creacion': info['creation-timestamp'],
            'grullas_id': grullas_id,
            'eventos_count': info['events-count'],
        }
        
def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    pass


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    pass


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    pass


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    pass


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    pass


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    pass

# Se crea la lógica asociado a la vista
control = new_logic()

# main del ejercicio
def main():
    """
    Menu principal
    """
    control = new_logic()
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 0:
            print("Cargando información de los archivos ....\n")
            control = load_data(control)
        elif int(inputs) == 1:
            print_req_1(control)

        elif int(inputs) == 2:
            print_req_2(control)

        elif int(inputs) == 3:
            print_req_3(control)

        elif int(inputs) == 4:
            print_req_4(control)

        elif int(inputs) == 5:
            print_req_5(control)

        elif int(inputs) == 5:
            print_req_6(control)

        elif int(inputs) == 7:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
