import osmnx as ox
import networkx as nx
from helper import get_node_using_name

class Node:
    def __init__(self, name, longitude, latitude):
        self.name = name
        self.longitude = longitude
        self.latitude = latitude

        self.connections = []

    def get_route_to_target(self, target_name: str):
        for connection in self.connections:
            if connection.target.name == target_name: return connection.route

    def get_distance_to_target(self, target_name: str):
        for connection in self.connections:
            if connection.target.name == target_name: return connection.distance

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
        for connection in source_node.connections:
            if max_distance < connection.distance:
                max_distance = connection.distance
                furthest_node = connection.target

        return furthest_node

    def simulate_optimal_route(self):
        routes = []
        
        # routes.append(get_node_using_name(self.nodes, "UPSIN").get_route_to_target("Monumento del Pescador"))
        routes.append(get_node_using_name(self.nodes, "Monumento del Pescador"))
        routes.append(get_node_using_name(self.nodes, "Punto Valentino's"))
        routes.append(get_node_using_name(self.nodes, "Walmart Ejercito Mexicano"))
        routes.append(get_node_using_name(self.nodes, "Telmex Av. Insurgentes"))
        routes.append(get_node_using_name(self.nodes, "Acuario"))
        routes.append(get_node_using_name(self.nodes, "Jefaturas de Servicios III Región Militar"))
        routes.append(get_node_using_name(self.nodes, "Panamá Restaurantes y Pastelerias"))
        routes.append(get_node_using_name(self.nodes, "Pesca Azteca"))
        routes.append(get_node_using_name(self.nodes, "UPSIN"))

        return routes

    def get_most_optimal_node_list(self, most_optimal_visited = [], visited = [], current_distance = 0, min_distance = float('inf')):  # We got humbled
        if len(visited) == 0:  # Initializer
            visited.append(self.source)

        for connection in visited[-1].connections:
            flag = True
            # If list completed, we're done
            if len(visited) == len(self.nodes):  # If all nodes have been visited, we go back
                return visited.copy()
            if connection.target in visited:  # If node is repeating, iteration is finished
                # print(f'Repeated node {connection.target.name} from {visited[-1].name}')
                flag = False
                # print("Nodo se repite")
            if len(visited) < len(self.nodes) - 1 and connection.target == self.target:  # If final target node is not at the and current node is target, we finish
                # visited.append(connection.target)
                # for x in visited:
                #     print(x.name)
                # visited.pop()
                # print(f'{connection.target.name} was ignored')
                flag = False
                # print("Nodo final aparece antes")
            
            if flag:
                # If list isn't full, we keep going
                visited_copy = visited[:]
                visited_copy.append(connection.target)
                current_distance += connection.distance
                # print(f'From {visited[-2].name} to {connection.target.name} theres {connection.distance}m')

                temp_list = self.get_most_optimal_node_list(most_optimal_visited, visited_copy, current_distance, min_distance)
                # for x in temp_list:
                #     print(x.name)
                # print(f'Current distance: {current_distance}')
                # print(f'Fn distance: {self.get_distance_from_node_list(temp_list)}')
                # print("-----------------------------")
                current_distance = self.get_distance_from_node_list(temp_list)  # curernt distance is all buggy
                if current_distance < self.get_distance_from_node_list(most_optimal_visited) or len(most_optimal_visited) == 0:
                    most_optimal_visited = temp_list
                    min_distance = current_distance
                # print('---------------------------------')
                # for x in temp_list:
                #     print(x.name)
                # print(f'Min distance: {current_distance}')
                # print('---------------------------------')
                # current_distance = 0
        return most_optimal_visited
    
    def get_distance_from_node_list(self, node_list):
        distance = 0
        try:
            for x in range(len(node_list) - 1):
                next_node = node_list[x + 1]
                distance += node_list[x].get_distance_to_target(next_node.name)
        except:
            return float('inf')
        return distance
    
    def get_routes_from_node_list(self, node_list):
        routes = []
        for x, node in enumerate(node_list):
            try:
                routes.append(node.get_route_to_target(node_list[x + 1].name))
            except:
                pass
        return routes

    # def get_route_from_node_list(self, node_list):

if __name__ == '__main__':
    # G = ox.graph_from_place('Mazatlán, Sinaloa, México', network_type='drive')
    address = 'Universidad Politécnica de Sinaloa, Calle Cerro de Guadalupe, Genaro Estrada, Mazatlán, Sinaloa, 82199, Mexico'
    G = ox.graph_from_address(address, dist=7500, network_type='drive')
    # fig, ax = ox.plot_graph(G, show=False, close=False)

    # Define the locations as Node objects
    locations = [
        Node("UPSIN", -106.37420308842162, 23.265557831781045),
        Node("Panamá Restaurantes y Pastelerias", -106.41613965222278, 23.21602192762802),
        Node("Monumento del Pescador", -106.42150523059132, 23.211686544028336),
        Node("Acuario", -106.41034974469306, 23.238435910234127),
        Node("Pesca Azteca", -106.39299053047824, 23.214415781178907),
        Node("Jefaturas de Servicios III Región Militar", -106.40823981422209, 23.22473048075688),
        Node("Walmart Ejercito Mexicano", -106.42349869463574, 23.245098749400867),
        Node("Punto Valentino's", -106.44580667740355, 23.238469795249422),
        Node("Telmex Av. Insurgentes", -106.41678831852965, 23.235330866471884)
    ]

    # BÚSQUEDA 
    epic = Graph(G)

    for location in locations:
        epic.add_node(location)

    source_node = get_node_using_name(locations, "UPSIN")
    furthest_node = epic.get_furthest_node_from_source_node(source_node)

    print(f'El nodo más lejano es {furthest_node.name}')

    epic.set_source(furthest_node) # Se empieza en el más lejano y se termina en la escuela
    epic.set_target(source_node)

    # Printing tree of 4 depth
    print("MONUMENTO")
    for connection in furthest_node.connections:
        print("├──", connection.target.name)
        for sub_connection in connection.target.connections:
            print("│   ├──", sub_connection.target.name)
            for sub_sub_connection in sub_connection.target.connections:
                print("│   │   ├──", sub_sub_connection.target.name)
                for sub_sub_connection in sub_connection.target.connections:
                    print("│   │   │   ├──", sub_sub_connection.target.name)

    # routes = epic.get_most_optimal_route()
    routes = epic.get_routes_from_node_list(epic.get_most_optimal_node_list())