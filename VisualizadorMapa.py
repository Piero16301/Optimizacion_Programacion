import plotly.graph_objects as go
import json


class VisualizadorMapa:
    def __init__(self, dataFrame):
        credenciales = json.load(open('credenciales.json'))
        self.mapboxToken = credenciales['keyMapbox']
        self.dataFrame = dataFrame
        self.mapa = go.Figure()

    def visualizarEstaciones(self):
        self.mapa = go.Figure(go.Scattermapbox(
            lat=self.dataFrame['Latitud'],
            lon=self.dataFrame['Longitud'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=10
            ),
            text=self.dataFrame['Estación']
        ))

        # Calcular centro del mapa
        promLatitud = self.dataFrame['Latitud'].mean()
        promLongitud = self.dataFrame['Longitud'].mean()

        self.mapa.update_layout(
            autosize=True,
            mapbox=dict(
                accesstoken=self.mapboxToken,
                center=dict(
                    lat=promLatitud,
                    lon=promLongitud
                ),
                style='streets',
                zoom=10
            ),
        )

        self.mapa.show()
