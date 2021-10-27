import plotly.graph_objects as go
import json


class VisualizadorMapa:
    def __init__(self, dataFrame):
        credenciales = json.load(open('archivos_json/credenciales.json'))
        self.mapboxToken = credenciales['keyMapbox']
        self.dataFrame = dataFrame
        self.mapa = go.Figure()

    def visualizarEstaciones(self, columnaTexto):
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
            autosize=True,
            mapbox=dict(
                accesstoken=self.mapboxToken,
                center=dict(
                    lat=promLatitud,
                    lon=promLongitud
                ),
                style='streets',
                zoom=12
            ),
        )

        self.mapa.show()
