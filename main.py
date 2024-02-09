import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

from classes import Node
from classes import Graph
from helper import get_node_using_name

# TODO
# En vez de UPSIN a un punto en concreto, que sea a varios puntos en concreto.
# Que aparezca cuánto cuesta el viaje total y nodo a nodo, ya que
    # Tiene que empezar en UPSIN
    # Tiene que terminar en UPSIN
    # Tiene que cruzar por la mayor cantidad de nodos posibles, si es posible TODOS
# Poner un límite de costos usando Heurísticas, un tipo de Prompt que limite el presupuesto por viaje

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

# Get UPSIN node
upsin_coords = (-106.37420308842162, 23.265557831781045)
upsin_node = ox.nearest_nodes(G, upsin_coords[0], upsin_coords[1])

# SE CALCULA LA DISTANCIA MÁS LEJANA
furthest_location = ''
furthest_distance = float('-inf')

for location in locations:
    if location.name != "UPSIN":
        target_node = ox.nearest_nodes(G, location.longitude, location.latitude)
        distance = round(nx.shortest_path_length(G, source=upsin_node, target=target_node, weight='length'), 2)
        if distance > furthest_distance:
            furthest_distance = distance
            furthest_location = location.name

print("Furthest location from UPSIN:", furthest_location)
print("Distance from UPSIN:", furthest_distance, "meters")

# Get nodes corresponding to the specified coordinates
source_node = get_node_using_name(locations, "UPSIN")
target_node = get_node_using_name(locations, furthest_location)

# Convert coordinates to nodes
source_node_graph = ox.nearest_nodes(G, source_node.longitude, source_node.latitude)
target_node_graph = ox.nearest_nodes(G, target_node.longitude, target_node.latitude)

# BÚSQUEDA 
epic = Graph(G, source=get_node_using_name(locations, furthest_location), target=get_node_using_name(locations, "UPSIN"))
for location in locations:
    epic.add_node(location)

routes = [connection.route for connection in epic.connections]

# route = nx.shortest_path(G, source=source_node_graph, target=target_node_graph, weight='length') # LSP's fault
fig, ax = ox.plot_graph_routes(G, routes, route_linewidth=0.1, node_size=3, route_colors='r', bgcolor='w', show=False, close=False)

plt.show()
