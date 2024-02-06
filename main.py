import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

from classes import Node
from helper import get_location_using_name

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
    target_node = ox.nearest_nodes(G, location.longitud, location.latitud)
    distance = round(nx.shortest_path_length(G, source=upsin_node, target=target_node, weight='length'), 2)
    if distance > furthest_distance:
        furthest_distance = distance
        furthest_location = location.nombre

print("Furthest location from UPSIN:", furthest_location)
print("Distance from UPSIN:", furthest_distance, "meters")

# Get nodes corresponding to the specified coordinates
source_coords = upsin_coords
target_coords = get_location_using_name(locations, furthest_location)

# Convert coordinates to nodes
source_node = ox.nearest_nodes(G, source_coords[0], source_coords[1])
target_node = ox.nearest_nodes(G, target_coords[0], target_coords[1])  # LSP's fault too lmao

route = nx.shortest_path(G, source=source_node, target=target_node, weight='travel_time') # LSP's fault
fig, ax = ox.plot_graph_route(G, route, route_linewidth=3, node_size=0, bgcolor='w', show=False, close=False)

# SCATTERING OF POINTS
# For some damn reason, longitude is first than latitude, like ??????????????
ax.scatter(-106.37420308842162, 23.265557831781045, c='blue')  # UPSIN
for location in locations:
    ax.scatter(location.longitud, location.latitud, c='blue')

plt.show()
