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

# print(f'El nodo más lejano es {furthest_node.name}')

epic.set_source(furthest_node) # Se empieza en el más lejano y se termina en la escuela
epic.set_target(source_node)

initial_route = get_node_using_name(locations, source_node.name).get_route_to_target(furthest_node.name)

# routes = epic.get_most_optimal_route()
# most_optimal_node_list = epic.simulate_optimal_route()
most_optimal_node_list = epic.get_most_optimal_node_list()

meters_to_km = lambda meters: meters / 1000

distance_meters = epic.get_distance_from_node_list(most_optimal_node_list)
distance_km = round(meters_to_km(distance_meters), 2)

distance_source_to_target_meters = get_node_using_name(locations, source_node.name).get_distance_to_target(furthest_node.name)
distance_source_to_target_km = round(meters_to_km(distance_source_to_target_meters), 2)

routes = epic.get_routes_from_node_list(most_optimal_node_list)
# routes = [connection.route for node in epic.nodes for connection in node.connections]

###
### STYLES
###

# Create a new figure with a fixed size
fig, ax = plt.subplots(figsize=(12, 12))  # Adjust the size as needed

# Annotate node names
for node in [source_node, furthest_node]:
    ax.annotate(node.name, (node.longitude, node.latitude), fontsize=6, ha='center')

# Load and plot the logo image
logo = plt.imread('src/logo.png')  # Replace 'src/logo.png' with the path to your logo image
logo_ax = fig.add_axes([0.8, 0.8, 0.2, 0.2])  # Adjust position and size as needed
logo_ax.imshow(logo)
logo_ax.axis('off')

# Add a title
ax.set_title(f'El punto más lejano de {source_node.name}', fontsize=16, fontweight='bold')

# Set a window title
fig.canvas.manager.set_window_title('El Sabio de las Rutas - SHITSU')

# Set dimensions to maximized
manager = plt.get_current_fig_manager()
manager.window.state('zoomed')  # Maximize the window

# Add informative text to the right of the plot
info_text = 'Lista a seguir:\n\n'
for node in most_optimal_node_list:
    info_text += f'  *   {node.name}\n\n'

plt.figtext(0.775, 0.5, info_text, fontsize=10, verticalalignment='center', horizontalalignment='left')

# Add informative text to the left of the plot
left_text = f"""
Nodo inicial:
 * {source_node.name}

Nodo más lejano:
 * {furthest_node.name}

Distancia {source_node.name} a punto más lejano:
 * {distance_source_to_target_km}km

Distancia punto más lejano a UPSIN:
 * {distance_km}km

Distancia completa:
 * {distance_source_to_target_km + distance_km}km
"""

plt.figtext(0.075, 0.5, left_text, fontsize=10, verticalalignment='center', horizontalalignment='left')

# Customize plot to resemble a map
ax.set_aspect('equal')
ax.set_facecolor('w')  # Set background color to white
ax.tick_params(left=False, bottom=False)  # Remove ticks

# Plot the initial route (green)
ox.plot_graph_route(G, initial_route, ax=ax, route_linewidth=1, node_size=3, route_colors='g', bgcolor='w', show=False, close=False)
plt.waitforbuttonpress()

# Plot subsequent routes with different colors (red)
ax.clear()

# Add a title
ax.set_title(f"La Mejor Ruta Hamiltoniana de {source_node.name} al punto más lejano", fontsize=16, fontweight='bold')

# Annotate node names
for node in epic.nodes:
    ax.annotate(node.name, (node.longitude, node.latitude), fontsize=6, ha='center')

# Routes are added
for route in routes:
    ox.plot_graph_route(G, route, ax=ax, route_linewidth=1, node_size=3, route_colors='r', bgcolor='w', show=False, close=False)
    
    # Annotate edge distances
    for u, v, data in G.edges(data=True):
        if (u, v) in route or (v, u) in route:
            distance = data['length']
            ax.annotate(f"{distance:.2f} m", ((u[1] + v[1]) / 2, (u[0] + v[0]) / 2), fontsize=6, ha='center')

# Display the final plot
plt.show()