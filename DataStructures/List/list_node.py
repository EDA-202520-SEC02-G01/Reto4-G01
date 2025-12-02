"""
  Estructura que contiene la información a guardar en una lista encadenada
"""


def new_single_node(element):
    """
    Crea un nodo simple (de tipo :ref:`list_node<list-node>`) con un elemento dado.

    El nodo es creado con los siguientes atributos:

    * **info**: información del nodo, inicializada con el elemento dado.
    * **next**: Referencia al siguiente nodo, inicializada en None.

    :param element: Elemento del nodo.
    :type element: any

    :returns: Nodo recien creado.
    :rtype: :ref:`list_node<list-node>`
    """
    node = {"info": element, "next": None}
    return node


def get_element(node):
    """
    Retorna la información del nodo.

   :param node: Nodo del cual se obtendrá la información.
   :type node: :ref:`list_node<list-node>`

   :returns: Información del nodo.
   :rtype: any
    """
    return node["info"]


def get_next(node):
    """
    Retorna la referencia al siguiente nodo.

   :param node: Nodo del cual se obtendrá la referencia al siguiente nodo.
   :type node: :ref:`list_node<list-node>`

   :returns: Referencia al siguiente nodo.
   :rtype: :ref:`list_node<list-node>`
   """
    return node["next"]


def new_double_node(element):
    """Estructura que contiene la información a guardar en un nodo de una lista doblemente encadenada"""
    node = {"info": element, "next": None, "prev": None}
    return