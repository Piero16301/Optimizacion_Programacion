import plotly.graph_objects as go
import json


class VisualizadorMapa:
    def __init__(self, dataFrame):
        credenciales = json.load(open('credenciales.json'))
        self.mapboxToken = credenciales['keyMapbox']
        self.dataFrame = dataFrame
        self.mapa = go.Figure()

    def visualizarEstaciones(self, columnaTexto):
        self.mapa = go.Figure(go.Scattermapbox(
            mode='markers',
            lat=self.dataFrame['Latitud'],
            lon=self.dataFrame['Longitud'],
            marker={
                'size': 10,
                'symbol': self.dataFrame['Símbolo']
            },
            text=self.dataFrame[columnaTexto]
        ))

        # self.mapa.update_traces(
        #     marker_symbol='fuel',
        #     selector=dict(
        #         type='scattermapbox'
        #     )
        # )

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
