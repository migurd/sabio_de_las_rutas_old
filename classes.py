from ast import List
from collections import deque
import osmnx as ox
import networkx as nx



class Node:
    def __init__(self, name, longitude, latitude):
        self.name = name
        self.longitude = longitude
        self.latitude = latitude

        self.lowest_value = float('inf')
        self.previous_node = None
        self.connections = []

    def get_route_to_target(self, target_name: str):
        for connection in self.connections:
            if connection.target.name == target_name: return connection.route

class Connection:
    def __init__(self, target: Node, distance: float, route):
        self.target = target
        self.distance = distance
        self.route = route

    def describe(self):
        print(f'{self.source.name:<50}{self.target.name}')

def get_node_using_name(node_lst: list[Node], name: str):
    for node in node_lst:
        if node.name == name:
            return node

class Graph:
    def __init__(self, G, source = None, target = None):
        self.G = G
        self.source = source
        self.target = target

        self.nodes = []

    def set_source(self, source: Node):
        self.source = source

    def set_target(self, target: Node):
        self.target = target

    def add_node(self, new_node: Node):
        if new_node in self.nodes:  # Node is NOT added to the list IF node is already listed
            return
        else:
            self.nodes.append(new_node)

        # Connection is created with all other nodes
        for node in self.nodes:
            if new_node != node:  # Nodes are not connected to themselves
                self.add_connection(new_node, node)

    def add_connection(self, source: Node, target: Node):
        source_node_graph = self.get_nearest_node(source)
        target_node_graph = self.get_nearest_node(target)  # Actual coordinates for the Graph are gotten
        distance = self.get_connection_distance(source_node_graph, target_node_graph)  # Real distance is gotten
        route = self.get_shortest_route(source_node_graph, target_node_graph)

        new_connection_from_source_to_target = Connection(target, distance, route)  # Heuristic connection using Distance is created
        new_connection_from_target_to_source = Connection(source, distance, route)

        source.connections.append(new_connection_from_source_to_target)  # Se añaden conexiones a los nodos
        target.connections.append(new_connection_from_target_to_source)
        # print(f'{source.name} está alejado de {target.name} por un total de {distance}m')

    def get_connection_distance(self, source, target):
        distance = nx.shortest_path_length(self.G, source=source, target=target, weight='length')
        return round(distance, 2)

    def get_shortest_route(self, source, target):
        return nx.shortest_path(self.G, source=source, target=target, weight='length')

    def get_nearest_node(self, node: Node):
        return ox.nearest_nodes(self.G, node.longitude, node.latitude)
    
    def get_furthest_node_from_source_node(self, source_node: Node):
        max_distance = 0
        furthest_node = None
        for connection in source_node.connections:
            if max_distance < connection.distance:
                max_distance = connection.distance
                furthest_node = connection.target

        return furthest_node

    def simulate_optimal_route(self):
        routes = []
        
        # routes.append(get_node_using_name(self.nodes, "UPSIN").get_route_to_target("Monumento del Pescador"))
        routes.append(get_node_using_name(self.nodes, "Monumento del Pescador").get_route_to_target("Punto Valentino's"))
        routes.append(get_node_using_name(self.nodes, "Punto Valentino's").get_route_to_target("Walmart Ejercito Mexicano"))
        routes.append(get_node_using_name(self.nodes, "Walmart Ejercito Mexicano").get_route_to_target("Telmex Av. Insurgentes"))
        routes.append(get_node_using_name(self.nodes, "Telmex Av. Insurgentes").get_route_to_target("Acuario"))
        routes.append(get_node_using_name(self.nodes, "Acuario").get_route_to_target("Jefaturas de Servicios III Región Militar"))
        routes.append(get_node_using_name(self.nodes, "Jefaturas de Servicios III Región Militar").get_route_to_target("Panamá Restaurantes y Pastelerias"))
        routes.append(get_node_using_name(self.nodes, "Panamá Restaurantes y Pastelerias").get_route_to_target("Pesca Azteca"))
        routes.append(get_node_using_name(self.nodes, "Pesca Azteca").get_route_to_target("UPSIN"))

        return routes

    def get_most_optimal_route(self):  # We got humbled
        pass