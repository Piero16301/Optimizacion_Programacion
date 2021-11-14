import json
from geopy.distance import geodesic
from statsmodels.graphics.plot_grids import scatter_ellipse


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
        self.grafo = []

    def buscar(self, padre, i):
        if padre[i] == i:
            return i
        return self.buscar(padre, padre[i])

    def unir(self, padre, rank, x, y):
        raizX = self.buscar(padre, x)
        raizY = self.buscar(padre, y)
        if rank[raizX] < rank[raizY]:
            padre[raizX] = raizY
        elif rank[raizX] > rank[raizY]:
            padre[raizY] = raizX
        else:
            padre[raizY] = raizX
            rank[raizX] += 1

    def kruskalMST(self, vertices):
        resultado = []
        i = 0
        e = 0
        self.grafo = sorted(self.grafo, key=lambda item: item[2])
        padre = []
        rank = []
        for nodo in range(vertices):
            padre.append(nodo)
            rank.append(0)
        while e < vertices - 1:
            u, v, w = self.grafo[i]
            i = i + 1
            x = self.buscar(padre, u)
            y = self.buscar(padre, v)
            if x != y:
                e = e + 1
                resultado.append([u, v, w])
                self.unir(padre, rank, x, y)
        # costoMinimo = 0
        # for u, v, peso in resultado:
        #     costoMinimo += peso
        return resultado

    def construirResultado(self, recorridoGlobal):
        recorrido = [['1002634', '3008006', 'P371'],
                     ['1002661', '1000435', '1012420'],
                     ['1012144', 'P125', '3002730']]
        unidades = ['AJF-705', 'B7K-982', 'AYR-771']

        return recorrido, unidades

    def calcularRutas(self):
        print('Calculando rutas óptimas...')
        estaciones = self.dataCOESTI['Centro'].unique().tolist()
        for i in range(len(estaciones)):
            for j in range(len(estaciones)):
                if i != j:
                    origen = (self.direcciones[estaciones[i]]['Latitud'], self.direcciones[estaciones[i]]['Longitud'])
                    destino = (self.direcciones[estaciones[j]]['Latitud'], self.direcciones[estaciones[j]]['Longitud'])
                    distancia = geodesic(origen, destino).kilometers
                    self.grafo.append([estaciones.index(estaciones[i]), estaciones.index(estaciones[j]), distancia])
        resultadoKruskal = self.kruskalMST(len(estaciones))

        # Ordenar las unidades de menor a mayor
        unidadesOrdenadas = sorted(self.unidades, key=lambda valor: self.unidades[valor]['Capacidad'])
        unidadesOrdenadasDict = {}
        for unidad in unidadesOrdenadas:
            unidadesOrdenadasDict[unidad] = self.unidades[unidad]
        self.unidades = unidadesOrdenadasDict

        # Convertir indices a nombres de estaciones
        recorridoGlobal = []
        for u, v, peso in resultadoKruskal:
            recorridoGlobal.append([estaciones[u], estaciones[v]])

        return self.construirResultado(recorridoGlobal)
