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

cantidadgrupos = 10
elementosPorGrupo = 15
estacionesPorElemento = 3

latitud = []
longitud = []
grupos = []

colores = ['aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque', 'black', 'blanchedalmond',
           'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral',
           'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray',
           'darkgrey', 'darkgreen', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid',
           'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'darkslategrey', 'darkturquoise',
           'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue', 'firebrick', 'floralwhite',
           'forestgreen', 'fuchsia', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'gray', 'grey', 'green',
           'greenyellow', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki', 'lavender', 'lavenderblush',
           'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgray',
           'lightgrey', 'lightgreen', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray',
           'lightslategrey', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 'magenta', 'maroon',
           'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue',
           'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose',
           'moccasin', 'navajowhite', 'navy', 'oldlace', 'olive', 'olivedrab', 'orange', 'orangered', 'orchid',
           'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink',
           'plum', 'powderblue', 'purple', 'red', 'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown',
           'seagreen', 'seashell', 'sienna', 'silver', 'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow',
           'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'turquoise', 'violet', 'wheat', 'white',
           'whitesmoke', 'yellow', 'yellowgreen']

for i in range(cantidadgrupos * elementosPorGrupo):
    latitudActual = []
    longitudActual = []
    for j in range(estacionesPorElemento):
        latitudActual.append(random.uniform(-12.0745, -11.9479))
        longitudActual.append(random.uniform(-77.1308, -76.9678))
    latitud.append(latitudActual)
    longitud.append(longitudActual)

for i in range(cantidadgrupos):
    grupos.append('Turno ' + str(i + 1))

for i in range(cantidadgrupos * elementosPorGrupo):
    fig.add_trace(go.Scattermapbox(
        legendgroup=grupos[i // elementosPorGrupo],
        legendgrouptitle={'font': {'color': 'brown', 'size': 15}, 'text': grupos[i // elementosPorGrupo]},
        name=str(i+1),
        mode='markers+lines',
        lat=latitud[i],
        lon=longitud[i],
        marker={'size': 15, 'symbol': 'fuel', 'color': colores[i]}
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
    legend=dict(
        title=dict(
            font=dict(
                color='black',
                size=20
            ),
            text='Unidades'
        )
    ),
    mapbox={
        'accesstoken': token,
        'center': {'lat': promedioLatitud, 'lon': promedioLongitud},
        'style': 'basic',
        'zoom': 11.5
    },
    showlegend=True
)

fig.show()
