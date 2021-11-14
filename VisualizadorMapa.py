import plotly.graph_objects as go
import osmnx as ox
import networkx as nx
from cryptography.fernet import Fernet
import json


class VisualizadorMapa:
    def __init__(self, dataFrame, recorrido, unidades):
        # Se desencripta la key de mapbox con la key de fernet
        credenciales = json.load(open('archivos_json/credenciales.json'))
        keyFernet = credenciales['keyFernet']
        keyMapbox = credenciales['keyMapbox']

        fernet = Fernet(bytes(keyFernet, 'UTF-8'))
        keyDesencriptada = fernet.decrypt(bytes(keyMapbox, 'UTF-8')).decode()

        self.direcciones = json.load(open('archivos_json/direcciones.json', encoding='utf8'))

        self.mapboxToken = keyDesencriptada

        self.dataFrame = dataFrame

        self.mapa = go.Figure()

        print('Cargando grafo del mapa...')
        self.grafo = ox.load_graphml('grafos/grafoLima.graphml')

        self.recorrido = recorrido
        self.unidades = unidades

        # Se encripta la key de mapbox con una nueva key de fernet
        keyFernet = Fernet.generate_key().decode()
        fernet = Fernet(keyFernet)
        keyMapbox = fernet.encrypt(keyDesencriptada.encode()).decode()

        nuevasCredenciales = {
            'keyFernet': keyFernet,
            'keyMapbox': keyMapbox
        }
        with open('archivos_json/credenciales.json', 'w', encoding='utf8') as credencialesJSON:
            json.dump(nuevasCredenciales, credencialesJSON, indent=4, ensure_ascii=False)

    def construirGrafo(self):
        pass
        # maxLatitud = self.dataFrame['Latitud'].max()
        # minLatitud = self.dataFrame['Latitud'].min()
        #
        # maxLongitud = self.dataFrame['Longitud'].max()
        # minLongitud = self.dataFrame['Longitud'].min()
        #
        # margenLatitud = 0.001789912
        # margenLongitud = 0.001814071
        #
        # norte = maxLatitud + margenLatitud
        # este = maxLongitud + margenLongitud
        # sur = minLatitud - margenLatitud
        # oeste = minLongitud - margenLongitud

        # G = ox.graph_from_bbox(norte, sur, este, oeste, network_type='drive')
        # ox.save_graphml(G, 'grafos/grafo.graphml')
        # G = ox.load_graphml('grafos/grafo.graphml')
        # ox.plot_graph(G)

    def construirCamino(self, ruta):
        # Construir un camino a partir de nodos
        nodosBorde = list(zip(ruta[:-1], ruta[1:]))
        lineas = []

        for u, v in nodosBorde:
            data = min(self.grafo.get_edge_data(u, v).values(), key=lambda x: x['length'])
            if 'geometry' in data:
                xs, ys = data['geometry'].xy
                lineas.append(list(zip(xs, ys)))
            else:
                x1 = self.grafo.nodes[u]['x']
                y1 = self.grafo.nodes[u]['y']
                x2 = self.grafo.nodes[v]['x']
                y2 = self.grafo.nodes[v]['y']
                linea = [(x1, y1), (x2, y2)]
                lineas.append(linea)

        return lineas

    def agregarCamino(self, recorridoUnidad, unidad):
        caminoTotal = []
        for i in range(len(recorridoUnidad) - 1):
            puntoOrigen = (
                self.direcciones[recorridoUnidad[i]]['Latitud'],
                self.direcciones[recorridoUnidad[i]]['Longitud']
            )
            puntoDestino = (
                self.direcciones[recorridoUnidad[i + 1]]['Latitud'],
                self.direcciones[recorridoUnidad[i + 1]]['Longitud']
            )

            nodoOrigen = ox.get_nearest_node(self.grafo, puntoOrigen)
            nodoDestino = ox.get_nearest_node(self.grafo, puntoDestino)

            ruta = nx.shortest_path(self.grafo, nodoOrigen, nodoDestino, weight='length')

            camino = self.construirCamino(ruta)
            caminoTotal = caminoTotal + camino

        if len(recorridoUnidad) == 1:
            # Se mueve 100m a la derecha
            nodoOrigen = ox.get_nearest_node(self.grafo, (
                self.direcciones[recorridoUnidad[0]]['Latitud'],
                self.direcciones[recorridoUnidad[0]]['Longitud'] + 0.0018204086027)
                                             )
            nodoDestino = ox.get_nearest_node(self.grafo, (
                self.direcciones[recorridoUnidad[0]]['Latitud'],
                self.direcciones[recorridoUnidad[0]]['Longitud'])
                                              )

            ruta = nx.shortest_path(self.grafo, nodoOrigen, nodoDestino, weight='length')

            camino = self.construirCamino(ruta)
            caminoTotal = caminoTotal + camino

        latitudes = []
        longitudes = []

        for i in range(len(caminoTotal)):
            z = list(caminoTotal[i])
            l1 = list(list(zip(*z))[0])
            l2 = list(list(zip(*z))[1])
            for j in range(len(l1)):
                latitudes.append(l2[j])
                longitudes.append(l1[j])

        self.mapa.add_trace(go.Scattermapbox(
            name=unidad,
            mode='lines',
            lat=latitudes,
            lon=longitudes,
            marker={'size': 10},
            line=dict(
                width=4
            )
        ))

    def visualizarEstaciones(self, columnaTexto):
        # Construir grafo para las rutas
        self.construirGrafo()

        # Iniciar las posiciones de los puntos
        self.mapa = go.Figure(go.Scattermapbox(
            mode='markers',
            showlegend=False,
            lat=self.dataFrame['Latitud'],
            lon=self.dataFrame['Longitud'],
            text=self.dataFrame[columnaTexto],
            marker={
                'symbol': self.dataFrame['Símbolo'],
                'size': 13,
                'color': 'brown'
            }
        ))

        # origenes = [(-12.05228029, -77.14360947), (-11.93553478, -77.12662366), (-12.13157737, -76.97689901)]
        # destinos = [(-12.116601, -77.04496341), (-11.97719639, -77.01030252), (-12.06775267, -76.94659696)]
        # unidades = ['AJF-705', 'B7K-982', 'AYR-771']
        # colores = ['blue', 'green', 'red']

        print('Construyendo caminos...')

        for i in range(len(self.recorrido)):
            self.agregarCamino(self.recorrido[i], self.unidades[i])

        # Calcular centro del mapa
        promLatitud = self.dataFrame['Latitud'].mean()
        promLongitud = self.dataFrame['Longitud'].mean()

        # Establecer configuraciones del mapa
        self.mapa.update_layout(
            margin={'l': 0, 't': 0, 'b': 0, 'r': 0},
            legend=dict(
                title=dict(
                    font=dict(
                        color='black',
                        size=20
                    ),
                    text='Unidades'
                )
            ),
            mapbox=dict(
                accesstoken=self.mapboxToken,
                center=dict(
                    lat=promLatitud,
                    lon=promLongitud
                ),
                style='basic',
                zoom=11
            ),
        )

        self.mapa.show()
