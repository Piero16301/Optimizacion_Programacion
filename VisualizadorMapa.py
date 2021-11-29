import plotly.graph_objects as go
import osmnx as ox
import networkx as nx
import json
import random

from cryptography.fernet import Fernet
from geopy.distance import geodesic
from timeit import default_timer as timer


class VisualizadorMapa:
    def __init__(self, recorrido, unidades, detallado):
        # Se desencripta la key de mapbox con la key de fernet
        credenciales = json.load(open('archivos_json/credenciales.json'))
        keyFernet = credenciales['keyFernet']
        keyMapbox = credenciales['keyMapbox']

        fernet = Fernet(bytes(keyFernet, 'UTF-8'))
        keyDesencriptada = fernet.decrypt(bytes(keyMapbox, 'UTF-8')).decode()

        self.direcciones = json.load(open('archivos_json/direcciones.json', encoding='utf8'))

        self.mapboxToken = keyDesencriptada

        self.mapa = go.Figure()

        self.grafo = ox.load_graphml('grafos/grafoLima.graphml')

        self.recorrido = recorrido
        self.unidades = unidades
        self.detallado = detallado

        self.colores = ['black', 'blue', 'blueviolet', 'brown', 'cadetblue', 'chocolate', 'coral', 'cornflowerblue',
                        'crimson', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgreen', 'darkmagenta', 'darkorange',
                        'darkorchid', 'darkred', 'darksalmon', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue',
                        'dimgray', 'dodgerblue', 'firebrick', 'forestgreen', 'fuchsia', 'goldenrod', 'gray', 'green',
                        'hotpink', 'indianred', 'indigo', 'lightcoral', 'lightsalmon', 'lightseagreen',
                        'lightslategray', 'limegreen', 'magenta', 'maroon', 'mediumblue', 'mediumorchid',
                        'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumvioletred', 'midnightblue', 'navy',
                        'olive', 'orange', 'orangered', 'orchid', 'palevioletred', 'peru', 'purple', 'red', 'rosybrown',
                        'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'sienna', 'slateblue',
                        'slategray', 'steelblue', 'teal', 'tomato', 'violet', 'yellowgreen']

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

    def construirCamino(self, ruta, detallado):
        if detallado:
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
        else:
            return ruta

    def construirCoordenadas(self, caminoTotal, detallado):
        if detallado:
            latitudes = []
            longitudes = []
            for i in range(len(caminoTotal)):
                z = list(caminoTotal[i])
                l1 = list(list(zip(*z))[0])
                l2 = list(list(zip(*z))[1])
                for j in range(len(l1)):
                    latitudes.append(l2[j])
                    longitudes.append(l1[j])
            return latitudes, longitudes
        else:
            latitudes = []
            longitudes = []
            for i in caminoTotal:
                punto = self.grafo.nodes[i]
                latitudes.append(punto['y'])
                longitudes.append(punto['x'])
            return latitudes, longitudes

    def agregarCamino(self, recorridoUnidad, unidad):
        caminoTotal = []
        distanciaTotal = 0
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
            distanciaActual = geodesic(puntoOrigen, puntoDestino).kilometers
            distanciaTotal = distanciaTotal + distanciaActual

            camino = self.construirCamino(ruta, detallado=self.detallado)
            caminoTotal = caminoTotal + camino

        if len(recorridoUnidad) == 1:
            # Se mueve 200m a la derecha
            nodoOrigen = ox.get_nearest_node(self.grafo, (
                self.direcciones[recorridoUnidad[0]]['Latitud'],
                self.direcciones[recorridoUnidad[0]]['Longitud'] + 0.0018204086027)
                                             )
            nodoDestino = ox.get_nearest_node(self.grafo, (
                self.direcciones[recorridoUnidad[0]]['Latitud'],
                self.direcciones[recorridoUnidad[0]]['Longitud'])
                                              )

            ruta = nx.shortest_path(self.grafo, nodoOrigen, nodoDestino, weight='length')

            camino = self.construirCamino(ruta, detallado=self.detallado)
            caminoTotal = caminoTotal + camino

        latitudes, longitudes = self.construirCoordenadas(caminoTotal, detallado=self.detallado)

        colorActual = random.choice(self.colores)

        self.mapa.add_trace(go.Scattermapbox(
            name=unidad,
            mode='lines',
            lat=latitudes,
            lon=longitudes,
            marker={
                'size': 10,
                'color': colorActual
            },
            line={
                'width': 4
            }
        ))

        self.colores.remove(colorActual)

        return distanciaTotal

    def extraerEstacionesRecorridas(self):
        estacionesDuplicadas = []
        for recorridoUnidad in self.recorrido:
            for estacionUnidad in recorridoUnidad:
                estacionesDuplicadas.append(estacionUnidad)
        estacionesUnicas = list(dict.fromkeys(estacionesDuplicadas))

        textos = []
        latitudes = []
        longitudes = []
        simbolos = []

        for estacion in estacionesUnicas:
            textos.append(self.direcciones[estacion]['Estación'])
            latitudes.append(self.direcciones[estacion]['Latitud'])
            longitudes.append(self.direcciones[estacion]['Longitud'])
            simbolos.append(self.direcciones[estacion]['Símbolo'])

        return textos, latitudes, longitudes, simbolos

    def visualizarEstaciones(self, separador, inicio):
        # Construir grafo para las rutas
        self.construirGrafo()

        # Iniciar las posiciones de los puntos
        tiempo = '{:.3f}'.format(round(timer() - inicio, 3))
        print(
            '{0: <50}'.format('   3.2. Agregando localizacion de estaciones'),
            separador * 30, '    ', '{0: >7}'.format(tiempo), 'segundos'
        )
        textos, latitudes, longitudes, simbolos = self.extraerEstacionesRecorridas()
        self.mapa = go.Figure(go.Scattermapbox(
            mode='markers',
            showlegend=False,
            text=textos,
            lat=latitudes,
            lon=longitudes,
            marker={
                'symbol': simbolos,
                'size': 13,
                'color': 'green'
            }
        ))

        tiempo = '{:.3f}'.format(round(timer() - inicio, 3))
        print(
            '{0: <50}'.format('   3.3. Construyendo caminos de cada unidad'),
            separador * 30, '    ', '{0: >7}'.format(tiempo), 'segundos'
        )

        distanciaTotal = 0
        for i in range(len(self.recorrido)):
            distanciaCamino = self.agregarCamino(self.recorrido[i], self.unidades[i])
            distanciaTotal = distanciaTotal + distanciaCamino

        stringDistanciaTotal = '        3.3.1. Distancia total: ' + str(round(distanciaTotal, 3)) + ' Km'
        tiempo = '{:.3f}'.format(round(timer() - inicio, 3))
        print(
            '{0: <50}'.format(stringDistanciaTotal),
            separador * 30, '    ', '{0: >7}'.format(tiempo), 'segundos'
        )

        stringPromedioUnidad = '        3.3.2. Promedio por unidad: ' + \
                               str(round(distanciaTotal / len(self.unidades), 3)) + ' Km'
        tiempo = '{:.3f}'.format(round(timer() - inicio, 3))
        print(
            '{0: <50}'.format(stringPromedioUnidad),
            separador * 30, '    ', '{0: >7}'.format(tiempo), 'segundos'
        )

        # Calcular centro del mapa
        promLatitud = sum(latitudes) / len(latitudes)
        promLongitud = sum(longitudes) / len(longitudes)

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
