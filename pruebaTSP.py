import mlrose
import json
import pandas as pd
from geopy.distance import geodesic
from timeit import default_timer as timer

# Inicio de tiempo
inicio = timer()

print('Flag 1')

direcciones = json.load(open('archivos_json/direcciones.json', encoding='utf8'))

dataCOESTI = pd.DataFrame(
    pd.read_excel('datos_intermedios/Data_Direcciones_COESTI.xlsx', sheet_name='Sheet1', header=0)
)

ordenDirecciones = dataCOESTI['Centro'].unique().tolist()

# Create list of city coordinates
coords_list = []
for key in ordenDirecciones:
    coords_list.append((direcciones[key]['Latitud'], direcciones[key]['Longitud']))

print('Flag 2')

# Initialize fitness function object using coords_list
fitness_coords = mlrose.TravellingSales(coords=coords_list)

# Create list of distances between pairs of cities
dist_list = []
for i in range(len(ordenDirecciones)):
    for j in range(len(ordenDirecciones)):
        if i != j:
            origen = (direcciones[ordenDirecciones[i]]['Latitud'], direcciones[ordenDirecciones[i]]['Longitud'])
            destino = (direcciones[ordenDirecciones[j]]['Latitud'], direcciones[ordenDirecciones[j]]['Longitud'])
            distancia = geodesic(origen, destino).kilometers
            dist_list.append((i, j, distancia))

print('Flag 3')

# Initialize fitness function object using dist_list
fitness_dists = mlrose.TravellingSales(distances=dist_list)

problem_fit = mlrose.TSPOpt(length=len(ordenDirecciones), fitness_fn=fitness_dists, maximize=False)

print('Flag 4')

best_state, best_fitness = mlrose.genetic_alg(problem_fit, mutation_prob=0.2, max_attempts=100, random_state=2)

fin = timer()

with open('datos_intermedios/rutaDistancias.txt', 'w') as ruta:
    for estacion in best_state:
        ruta.write(str(ordenDirecciones[estacion]) + '\n')

print('The best state found is: ', best_state)

print('The fitness at the best state is: ', best_fitness)

print('Tiempo total:', round(fin - inicio, 2), 'segundos')

"""
import osmnx as ox
import networkx as nx
import osmnx.distance

grafo = ox.load_graphml('grafos/grafoLima.graphml')

# nodoOrigen = ox.get_nearest_node(grafo, (-12.1159933510202, -77.0185450896413))
# nodoDestino = ox.get_nearest_node(grafo, (-12.0900593087825, -77.0204967357459))

nodoOrigen = ox.get_nearest_node(grafo, (-12.090479833549857, -77.01985679645446))
nodoDestino = ox.get_nearest_node(grafo, (-12.0936089048694, -76.96733134229191))

ruta = nx.dijkstra_path(grafo, nodoOrigen, nodoDestino, weight='length')
print(ruta)
"""
