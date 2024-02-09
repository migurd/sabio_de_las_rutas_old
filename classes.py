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

class Connection:
    def __init__(self, target: Node, distance: float, route):
        self.target = target
        self.distance = distance
        self.route = route

    def describe(self):
        print(f'{self.source.name:<50}{self.target.name}')

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
        print("hi")
        for connection in source_node.connections:
            if max_distance < connection.distance:
                max_distance = connection.distance
                furthest_node = connection.target

        return furthest_node

    def get_most_optimal_path(self):  # Returns path list
        most_optimal_path = []  # Connections that start from the furthest point and finishes at school

        # Búsqueda de Anchura
        # It has two rules tho
        # 1. It has to cover all the nodes
        # 2. The last node is UPSIN and first one is source
        
        # Se inicializan las distancias
        self.source.lowest_value = 0
        total_distance = 0

        # 
        
        
        return most_optimal_path







