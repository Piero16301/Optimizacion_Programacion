import plotly.graph_objects as go
import osmnx as ox
import networkx as nx
import json


class VisualizadorMapa:
    def __init__(self, dataFrame):
        credenciales = json.load(open('archivos_json/credenciales.json'))
        self.mapboxToken = credenciales['keyMapbox']
        self.dataFrame = dataFrame
        self.mapa = go.Figure()
        self.grafo = ox.load_graphml('pruebas/grafoLima.graphml')

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
        # ox.save_graphml(G, 'pruebas/grafo.graphml')
        # G = ox.load_graphml('pruebas/grafo.graphml')
        # ox.plot_graph(G)

    def agregarCamino(self, origen, destino, unidad, color):
        puntoOrigen = origen
        puntoDestino = destino

        nodoOrigen = ox.get_nearest_node(self.grafo, puntoOrigen)
        nodoDestino = ox.get_nearest_node(self.grafo, puntoDestino)

        ruta = nx.shortest_path(self.grafo, nodoOrigen, nodoDestino, weight='length')

        latitudes = []
        longitudes = []

        for i in ruta:
            punto = self.grafo.nodes[i]
            latitudes.append(punto['y'])
            longitudes.append(punto['x'])

        self.mapa.add_trace(go.Scattermapbox(
            name=unidad,
            mode='lines',
            lat=latitudes,
            lon=longitudes,
            marker={'size': 10},
            line=dict(
                width=3,
                color=color
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

        origenes = [(-12.05228029, -77.14360947), (-11.93553478, -77.12662366), (-12.13157737, -76.97689901)]
        destinos = [(-12.116601, -77.04496341), (-11.97719639, -77.01030252), (-12.06775267, -76.94659696)]
        unidades = ['AJF-705', 'B7K-982', 'AYR-771']
        colores = ['blue', 'green', 'red']

        for i in range(len(origenes)):
            self.agregarCamino(origenes[i], destinos[i], unidades[i], colores[i])

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
                style='streets',
                zoom=11
            ),
        )

        self.mapa.show()
