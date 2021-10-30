import plotly.graph_objects as go
import osmnx as ox
import json


class VisualizadorMapa:
    def __init__(self, dataFrame):
        credenciales = json.load(open('archivos_json/credenciales.json'))
        self.mapboxToken = credenciales['keyMapbox']
        self.dataFrame = dataFrame
        self.mapa = go.Figure()

    def construirGrafo(self):
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
        G = ox.load_graphml('pruebas/grafo.graphml')
        # ox.plot_graph(G)

    def visualizarEstaciones(self, columnaTexto):
        # Construir grafo para las rutas
        self.construirGrafo()

        # Iniciar las posiciones de los puntos
        self.mapa = go.Figure(go.Scattermapbox(
            mode='markers',
            lat=self.dataFrame['Latitud'],
            lon=self.dataFrame['Longitud'],
            text=self.dataFrame[columnaTexto]
        ))

        # Establecer los símbolos de las estaciones
        self.mapa.update_traces(
            marker_symbol=self.dataFrame['Símbolo'],
            marker_size=13,
            marker_color='brown',
            selector=dict(
                type='scattermapbox'
            )
        )

        # Calcular centro del mapa
        promLatitud = self.dataFrame['Latitud'].mean()
        promLongitud = self.dataFrame['Longitud'].mean()

        # Establecer configuraciones del mapa
        self.mapa.update_layout(
            margin={'l': 0, 't': 0, 'b': 0, 'r': 0},
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

        # self.mapa.show()
