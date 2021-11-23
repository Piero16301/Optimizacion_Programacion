import json
from timeit import default_timer as timer
import mlrose
from geopy.distance import geodesic


def unirUnidades():
    unidades = {}

    unidadesTranscord = json.load(open('archivos_json/transcord.json', encoding='utf8'))
    unidadesLTP = json.load(open('archivos_json/ltp.json', encoding='utf8'))
    unidadesApoyo = json.load(open('archivos_json/apoyo.json', encoding='utf8'))

    # Se unen todas las flotas en una sola
    unidades.update(unidadesTranscord)
    unidades.update(unidadesLTP)
    unidades.update(unidadesApoyo)

    return unidades


def guardarRutaTSP(rutaArchivo, TSP, distancia):
    with open(rutaArchivo, 'w') as ruta:
        for estacion in TSP:
            ruta.write(str(estacion) + '\n')
        ruta.write('{:.3f}'.format(round(distancia, 3)) + '\n')
    ruta.close()


def cargarRutaTSP(rutaArchivo):
    TSP = []
    with open(rutaArchivo, 'r') as ruta:
        elemento = ' '
        for estacion in ruta:
            if elemento != ' ':
                TSP.append(int(elemento))
            elemento = str(estacion.strip())
        distancia = float(elemento)
    ruta.close()
    return TSP, distancia


class ProcesamientoRutas:
    def __init__(self, dataCOESTI, dataExternos):
        self.dataCOESTI = dataCOESTI
        self.dataExternos = dataExternos
        self.direcciones = json.load(open('archivos_json/direcciones.json', encoding='utf8'))
        self.unidades = unirUnidades()

    def optimizacionRutaMayor(self, recorridoGlobal):
        maximaDistancia = 0
        indiceMaximo = 0

        for i in range(len(recorridoGlobal)):
            if i == len(recorridoGlobal) - 1:
                origen = (
                    self.direcciones[recorridoGlobal[i]]['Latitud'],
                    self.direcciones[recorridoGlobal[i]]['Longitud']
                )
                destino = (
                    self.direcciones[recorridoGlobal[0]]['Latitud'],
                    self.direcciones[recorridoGlobal[0]]['Longitud']
                )
            else:
                origen = (
                    self.direcciones[recorridoGlobal[i]]['Latitud'],
                    self.direcciones[recorridoGlobal[i]]['Longitud']
                )
                destino = (
                    self.direcciones[recorridoGlobal[i + 1]]['Latitud'],
                    self.direcciones[recorridoGlobal[i + 1]]['Longitud']
                )

            if geodesic(origen, destino).kilometers > maximaDistancia:
                maximaDistancia = geodesic(origen, destino).kilometers
                indiceMaximo = i

        if indiceMaximo != (len(recorridoGlobal) - 1):
            nuevoRecorridoGlobal = []
            for i in range(indiceMaximo + 1, len(recorridoGlobal)):
                nuevoRecorridoGlobal.append(recorridoGlobal[i])

            for i in range(indiceMaximo + 1):
                nuevoRecorridoGlobal.append(recorridoGlobal[i])

            return nuevoRecorridoGlobal
        else:
            return recorridoGlobal

    def distribuirUnidades(self, recorridoGlobal):
        recorrido = []
        unidades = []

        rutaActual = []

        listaUnidades = list(self.unidades.keys())
        capacidades = [self.unidades[key]['Capacidad'] for key in self.unidades]
        unidadLlenando = 0
        for estacion in recorridoGlobal:
            if estacion[0] == 'P':
                pedido = self.dataCOESTI[self.dataCOESTI['Centro'] == estacion]['Sugerido'].sum()
            else:
                pedido = \
                    self.dataExternos[self.dataExternos['Solicitante'] == int(estacion)]['Cantidad de pedido'].sum()
            while pedido > 0.0:
                if pedido <= capacidades[unidadLlenando]:
                    capacidades[unidadLlenando] = capacidades[unidadLlenando] - pedido

                    rutaActual.append(estacion)

                    pedido = pedido - pedido
                else:
                    pedido = pedido - capacidades[unidadLlenando]
                    capacidades[unidadLlenando] = capacidades[unidadLlenando] - capacidades[unidadLlenando]

                    rutaActual.append(estacion)

                    recorrido.append([i for i in rutaActual])
                    unidades.append(listaUnidades[unidadLlenando])

                    rutaActual.clear()

                    unidadLlenando = unidadLlenando + 1

        return recorrido, unidades

    def optimizarRutasUnidades(self, recorrido):
        for i in range(len(recorrido)):
            if len(recorrido[i]) > 2:
                recorridoActual = recorrido[i]
                maximaDistancia = 0
                indiceMaximo = 0
                for j in range(len(recorridoActual)):
                    if j == len(recorridoActual) - 1:
                        origen = (
                            self.direcciones[recorridoActual[j]]['Latitud'],
                            self.direcciones[recorridoActual[j]]['Longitud']
                        )
                        destino = (
                            self.direcciones[recorridoActual[0]]['Latitud'],
                            self.direcciones[recorridoActual[0]]['Longitud']
                        )
                    else:
                        origen = (
                            self.direcciones[recorridoActual[j]]['Latitud'],
                            self.direcciones[recorridoActual[j]]['Longitud']
                        )
                        destino = (
                            self.direcciones[recorridoActual[j + 1]]['Latitud'],
                            self.direcciones[recorridoActual[j + 1]]['Longitud']
                        )

                    if geodesic(origen, destino).kilometers > maximaDistancia:
                        maximaDistancia = geodesic(origen, destino).kilometers
                        indiceMaximo = j

                if indiceMaximo != (len(recorridoActual) - 1):
                    nuevoRecorridoActual = []
                    for j in range(indiceMaximo + 1, len(recorridoActual)):
                        nuevoRecorridoActual.append(recorridoActual[j])

                    for j in range(indiceMaximo + 1):
                        nuevoRecorridoActual.append(recorridoActual[j])

                    recorrido[i] = nuevoRecorridoActual

        return recorrido

    def calcularRutas(self, separador, inicio):
        estacionesCOESTI = self.dataCOESTI['Centro'].unique().tolist()
        estacionesExternos = list(map(str, self.dataExternos['Solicitante'].unique().tolist()))
        estaciones = estacionesCOESTI + estacionesExternos
        # estaciones = estacionesCOESTI

        estacionesExistentes = []
        for estacion in estaciones:
            if estacion in self.direcciones:
                estacionesExistentes.append(estacion)
        estaciones = estacionesExistentes

        tiempo = '{:.3f}'.format(round(timer() - inicio, 3))
        print(
            '{0: <50}'.format('   2.1. Calculando distancias entre estaciones'),
            separador * 30, '    ', '{0: >7}'.format(tiempo), 'segundos'
        )

        # Construir lista de distancias
        distanciasEstaciones = []
        for i in range(len(estaciones)):
            for j in range(len(estaciones)):
                if i != j:
                    origen = (
                        self.direcciones[str(estaciones[i])]['Latitud'],
                        self.direcciones[str(estaciones[i])]['Longitud']
                    )
                    destino = (
                        self.direcciones[str(estaciones[j])]['Latitud'],
                        self.direcciones[str(estaciones[j])]['Longitud']
                    )
                    distancia = geodesic(origen, destino).kilometers
                    distanciasEstaciones.append((i, j, distancia))

        tiempo = '{:.3f}'.format(round(timer() - inicio, 3))
        print(
            '{0: <50}'.format('   2.2. Construyendo recorrido óptimo'),
            separador * 30, '    ', '{0: >7}'.format(tiempo), 'segundos'
        )

        # Construir recorrido TSP
        funcionConveniencia = mlrose.TravellingSales(distances=distanciasEstaciones)
        ajusteProblema = mlrose.TSPOpt(length=len(estaciones), fitness_fn=funcionConveniencia, maximize=False)
        posicionesRecorrido, distanciaGlobal = mlrose.genetic_alg(
            ajusteProblema, mutation_prob=0.2, max_attempts=100, random_state=2
        )

        guardarRutaTSP('datos_intermedios/rutaTSP.txt', posicionesRecorrido, distanciaGlobal)

        posicionesRecorrido, distanciaGlobal = cargarRutaTSP('datos_intermedios/rutaTSP.txt')

        stringDistanciaTotal = '        2.2.1. Distancia total: ' + str(round(distanciaGlobal, 3)) + ' Km'
        tiempo = '{:.3f}'.format(round(timer() - inicio, 3))
        print(
            '{0: <50}'.format(stringDistanciaTotal),
            separador * 30, '    ', '{0: >7}'.format(tiempo), 'segundos'
        )

        # Convertir posiciones a codigos de estación
        recorridoGlobal = []
        for i in range(len(posicionesRecorrido)):
            recorridoGlobal.append(estaciones[posicionesRecorrido[i]])

        recorridoGlobal = self.optimizacionRutaMayor(recorridoGlobal)

        tiempo = '{:.3f}'.format(round(timer() - inicio, 3))
        print(
            '{0: <50}'.format('   2.3. Ordenando unidades'),
            separador * 30, '    ', '{0: >7}'.format(tiempo), 'segundos'
        )

        # Ordenar las unidades de menor a mayor
        unidadesOrdenadas = sorted(self.unidades, key=lambda valor: self.unidades[valor]['Capacidad'], reverse=False)
        unidadesOrdenadasDict = {}
        for unidad in unidadesOrdenadas:
            unidadesOrdenadasDict[unidad] = self.unidades[unidad]
        self.unidades = unidadesOrdenadasDict

        tiempo = '{:.3f}'.format(round(timer() - inicio, 3))
        print(
            '{0: <50}'.format('   2.4. Distribuyendo unidades'),
            separador * 30, '    ', '{0: >7}'.format(tiempo), 'segundos'
        )

        recorrido, unidades = self.distribuirUnidades(recorridoGlobal)
        recorrido = self.optimizarRutasUnidades(recorrido)

        return recorrido, unidades
