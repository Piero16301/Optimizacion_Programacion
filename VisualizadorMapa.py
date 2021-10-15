import plotly.graph_objects as go


class VisualizadorMapa:
    def __init__(self, dataFrame):
        self.mapboxToken =\
            'pk.eyJ1IjoicGllcm8xNjMwMSIsImEiOiJja3VzbDgwbWE1Zzg0MzBxajFtN2tzcDVtIn0.Xlc1UX7d_VVo4LzfmKhumw'
        self.dataFrame = dataFrame

    def visualizarEstaciones(self):
        mapa = go.Figure(go.Scattermapbox(
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

        mapa.update_layout(
            autosize=True,
            mapbox=dict(
                accesstoken=self.mapboxToken,
                center=dict(
                    lat=promLatitud,
                    lon=promLongitud
                ),
                style='satellite-streets',
                zoom=10
            ),
        )

        mapa.show()
