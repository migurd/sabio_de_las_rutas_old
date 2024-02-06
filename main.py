import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

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
fig, ax = ox.plot_graph(G, show=False, close=False)

# Get nodes corresponding to the specified coordinates
source_coords = (-106.37420308842162, 23.265557831781045)
target_coords = (-106.41613965222278, 23.21602192762802)

# Convert coordinates to nodes
source_node = ox.nearest_nodes(G, source_coords[0], source_coords[1])
target_node = ox.nearest_nodes(G, target_coords[0], target_coords[1])

route = nx.shortest_path(G, source=source_node, target=target_node, weight='travel_time') # LSP's fault
fig, ax = ox.plot_graph_route(G, route, route_linewidth=3, node_size=0, bgcolor='w', show=False, close=False)

# ax.scatter(-106.37398, 23.26611, c='red')
# For some damn reason, longitude is first than latitude, like ??????????????
ax.scatter(-106.37420308842162, 23.265557831781045, c='red')  # UPSIN
ax.scatter(-106.41613965222278, 23.21602192762802, c='red')  # Panamá Restaurantes y Pastelerias Av. Ejercitos Mexicanos
ax.scatter(-106.42150523059132, 23.211686544028336, c='red')  # Monumento del Pescador
ax.scatter(-106.41034974469306, 23.238435910234127, c='red')  # Acuario
ax.scatter(-106.39299053047824, 23.214415781178907, c='red')  # Pesca Azteca
ax.scatter(-106.40823981422209, 23.22473048075688, c='red')  # Jefaturas de Servicios III Región Militar
ax.scatter(-106.42349869463574, 23.245098749400867, c='red')  # Walmart Ejercito Mexicano
ax.scatter(-106.44580667740355, 23.238469795249422, c='red')  # Punto Valentino's
ax.scatter(-106.41678831852965, 23.235330866471884, c='red')  # Telmex Av. Insurgentes

plt.show()
