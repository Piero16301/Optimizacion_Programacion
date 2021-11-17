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

    def calcularRutas(self, separador, inicio):
        estacionesCOESTI = self.dataCOESTI['Centro'].unique().tolist()
        estacionesExternos = self.dataExternos['Documento comercial'].unique().tolist()
        # estaciones = estacionesCOESTI + estacionesExternos
        estaciones = estacionesCOESTI

        tiempo = '{:.3f}'.format(round(timer() - inicio, 3))
        print(
            '{0: <50}'.format('   2.1. Calculando distancias entre estaciones'),
            separador * 30, '\t', '{0: >7}'.format(tiempo), 'segundos'
        )

        # Construir lista de distancias
        distanciasEstaciones = []
        for i in range(len(estaciones)):
            for j in range(len(estaciones)):
                if i != j:
                    origen = (self.direcciones[estaciones[i]]['Latitud'], self.direcciones[estaciones[i]]['Longitud'])
                    destino = (self.direcciones[estaciones[j]]['Latitud'], self.direcciones[estaciones[j]]['Longitud'])
                    distancia = geodesic(origen, destino).kilometers
                    distanciasEstaciones.append((i, j, distancia))

        tiempo = '{:.3f}'.format(round(timer() - inicio, 3))
        print(
            '{0: <50}'.format('   2.2. Construyendo recorrido óptimo'),
            separador * 30, '\t', '{0: >7}'.format(tiempo), 'segundos'
        )

        # Construir recorrido TSP
        funcionConveniencia = mlrose.TravellingSales(distances=distanciasEstaciones)
        ajusteProblema = mlrose.TSPOpt(length=len(estaciones), fitness_fn=funcionConveniencia, maximize=False)
        posicionesRecorrido, distanciaGlobal = mlrose.genetic_alg(
            ajusteProblema, mutation_prob=0.2, max_attempts=100, random_state=2
        )

        stringDistanciaTotal = '        2.2.1. Distancia total: ' + str(round(distanciaGlobal, 3)) + ' Km'
        tiempo = '{:.3f}'.format(round(timer() - inicio, 3))
        print(
            '{0: <50}'.format(stringDistanciaTotal),
            separador * 30, '\t', '{0: >7}'.format(tiempo), 'segundos'
        )

        # Convertir posiciones a codigos de estación
        recorridoGlobal = []
        for i in range(len(posicionesRecorrido)):
            recorridoGlobal.append(estaciones[posicionesRecorrido[i]])

        recorridoGlobal = self.optimizacionRutaMayor(recorridoGlobal)

        tiempo = '{:.3f}'.format(round(timer() - inicio, 3))
        print(
            '{0: <50}'.format('   2.3. Ordenando unidades'),
            separador * 30, '\t', '{0: >7}'.format(tiempo), 'segundos'
        )

        # Ordenar las unidades de menor a mayor
        unidadesOrdenadas = sorted(self.unidades, key=lambda valor: self.unidades[valor]['Capacidad'])
        unidadesOrdenadasDict = {}
        for unidad in unidadesOrdenadas:
            unidadesOrdenadasDict[unidad] = self.unidades[unidad]
        self.unidades = unidadesOrdenadasDict

        tiempo = '{:.3f}'.format(round(timer() - inicio, 3))
        print(
            '{0: <50}'.format('   2.4. Distribuyendo unidades'),
            separador * 30, '\t', '{0: >7}'.format(tiempo), 'segundos'
        )

        recorrido = []
        for i in range(len(recorridoGlobal) - 1):
            recorrido.append([recorridoGlobal[i], recorridoGlobal[i + 1]])

        return recorrido, list(range(1, len(recorridoGlobal)))
