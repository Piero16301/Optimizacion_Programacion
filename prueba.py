import plotly.graph_objects as go

fig = go.Figure(go.Scattermapbox(
    name='AJF-705',
    mode="markers+lines",
    lat=[-12.05228029, -12.0643958, -12.116601],
    lon=[-77.14360947, -77.11244219, -77.04496341],
    text=['Estación 1', 'Estación 2', 'Estación 3'],
    marker={'size': 13, 'symbol': 'fuel', 'color': 'blue'}
))

fig.add_trace(go.Scattermapbox(
    name='B7K-982',
    mode="markers+lines",
    lat=[-11.93553478, -11.9769313, -11.97719639],
    lon=[-77.12662366, -77.06032838, -77.01030252],
    text=['Estación 4', 'Estación 5', 'Estación 6'],
    marker={'size': 13, 'symbol': 'fuel', 'color': 'green'}
))

fig.add_trace(go.Scattermapbox(
    name='AYR-771',
    mode="markers+lines",
    lat=[-12.13157737, -12.12376978, -12.06775267],
    lon=[-76.97689901, -76.87217351, -76.94659696],
    text=['Estación 7', 'Estación 8', 'Estación 9'],
    marker={'size': 13, 'symbol': 'fuel', 'color': 'red'}
))

fig.update_layout(
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
        accesstoken='pk.eyJ1IjoicGllcm8xNjMwMSIsImEiOiJja3VzbDgwbWE1Zzg0MzBxajFtN2tzcDVtIn0.Xlc1UX7d_VVo4LzfmKhumw',
        center=dict(
            lat=-12.04335806012358,
            lon=-77.018094430038
        ),
        style='streets',
        zoom=11
    ),
)

fig.show()
