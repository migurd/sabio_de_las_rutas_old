import osmnx as ox
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

# BÚSQUEDA 
epic = Graph(G)

for location in locations:
    epic.add_node(location)

source_node = get_node_using_name(locations, "UPSIN")
furthest_node = epic.get_furthest_node_from_source_node(source_node)

print(f'El nodo más lejano es {furthest_node.name}')

epic.set_source(furthest_node) # Se empieza en el más lejano y se termina en la escuela
epic.set_target(source_node)

# routes = epic.get_most_optimal_route()
most_optimal_node_list = epic.simulate_optimal_route()
# most_optimal_node_list = epic.get_most_optimal_node_list()
print(epic.get_distance_from_node_list(most_optimal_node_list))
routes = epic.get_routes_from_node_list(most_optimal_node_list)
# routes = [connection.route for node in epic.nodes for connection in node.connections]



# Create a new figure and axis
fig, ax = plt.subplots()

for i, route in enumerate(routes):
    # Plot the graph with the current route
    ox.plot_graph_route(G, route, ax=ax, route_linewidth=1, node_size=3, route_colors='r', bgcolor='w', show=False, close=False)
    
    # Annotate edge distances
    for u, v, data in G.edges(data=True):
        if (u, v) in route or (v, u) in route:
            distance = data['length']
            ax.annotate(f"{distance:.2f} m", ((u[1] + v[1]) / 2, (u[0] + v[0]) / 2), fontsize=6, ha='center')

    # Annotate node names
    for node in epic.nodes:
        ax.annotate(node.name, (node.longitude, node.latitude), fontsize=6, ha='center')

    # Pause for 1 second
    plt.pause(0.2)

# Display the final plot
plt.show()