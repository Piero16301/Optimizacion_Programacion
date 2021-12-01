import plotly.graph_objects as go
import json
from cryptography.fernet import Fernet
import random

credenciales = json.load(open('archivos_json/credenciales.json'))
keyFernet = credenciales['keyFernet']
keyMapbox = credenciales['keyMapbox']

fernet = Fernet(bytes(keyFernet, 'UTF-8'))
token = fernet.decrypt(bytes(keyMapbox, 'UTF-8')).decode()

fig = go.Figure()

cantidadgrupos = 7
elementosPorGrupo = 10
estacionesPorElemento = 3

latitud = []
longitud = []
grupos = []

colores = ['blue', 'brown', 'chocolate', 'crimson', 'darkcyan', 'darkgoldenrod', 'darkorange',
           'darkorchid', 'darkturquoise', 'darkviolet', 'deeppink', 'dodgerblue', 'goldenrod', 'limegreen',
           'magenta', 'orange', 'red', 'royalblue', 'seagreen', 'tomato', 'black', 'blueviolet',
           'cadetblue', 'coral', 'cornflowerblue', 'darkblue', 'darkgreen', 'darkmagenta', 'darkred',
           'darksalmon', 'deepskyblue', 'dimgray', 'firebrick', 'forestgreen', 'fuchsia', 'gray', 'green',
           'hotpink', 'indianred', 'indigo', 'lightcoral', 'lightsalmon', 'lightseagreen',
           'lightslategray', 'maroon', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen',
           'mediumslateblue', 'mediumvioletred', 'midnightblue', 'navy', 'olive', 'orangered', 'orchid',
           'palevioletred', 'peru', 'purple', 'rosybrown', 'saddlebrown', 'salmon', 'sandybrown', 'sienna',
           'slateblue', 'slategray', 'steelblue', 'teal', 'violet', 'yellowgreen']

for i in range(cantidadgrupos * elementosPorGrupo):
    latitudActual = []
    longitudActual = []
    for j in range(estacionesPorElemento):
        latitudActual.append(random.uniform(-12.0745, -11.9479))
        longitudActual.append(random.uniform(-77.1308, -76.9678))
    latitud.append(latitudActual)
    longitud.append(longitudActual)

for i in range(cantidadgrupos):
    grupos.append('Vuelta ' + str(i + 1))

for i in range(cantidadgrupos * elementosPorGrupo):
    fig.add_trace(go.Scattermapbox(
        legendgroup=grupos[i // elementosPorGrupo],
        legendgrouptitle={'font': {'color': 'black', 'size': 15}, 'text': grupos[i // elementosPorGrupo]},
        name=colores[i],
        mode='markers+lines',
        lat=latitud[i],
        lon=longitud[i],
        marker={'size': 15, 'symbol': 'fuel', 'color': colores[i]},
        line={'width': 4}
    ))

totalLatitudes = []
totalLongitudes = []

for a in range(len(latitud)):
    totalLatitudes = totalLatitudes + latitud[a]
    totalLongitudes = totalLongitudes + longitud[a]

promedioLatitud = sum(totalLatitudes) / len(totalLatitudes)
promedioLongitud = sum(totalLongitudes) / len(totalLongitudes)

fig.update_layout(
    margin={'l': 0, 't': 0, 'b': 0, 'r': 0},
    legend={
        'title': {'font': {'color': 'black', 'size': 20}, 'text': 'Unidades'}
    },
    mapbox={
        'accesstoken': token,
        'center': {'lat': promedioLatitud, 'lon': promedioLongitud},
        'style': 'basic',
        'zoom': 11.5
    },
    showlegend=True
)

fig.show()
