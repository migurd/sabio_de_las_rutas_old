from typing import List
from classes import Node

def get_node_using_name(node_lst: List[Node], name: str):
    for node in node_lst:
        if node.name == name:
            return node
