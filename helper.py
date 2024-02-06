from typing import List
from classes import Node

def get_location_using_name(node_lst: List[Node], name: str):
    for node in node_lst:
        if node.nombre == name:
            return node.longitud, node.latitud
