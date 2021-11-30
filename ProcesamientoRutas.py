import json
from timeit import default_timer as timer
import mlrose
import pandas as pd
from geopy.distance import geodesic


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


def buscarSiguienteCompartimento(tipo, capacidadCompartimento, tiposCombustible):
    for i in range(len(tiposCombustible)):
        if tiposCombustible[i] == tipo and capacidadCompartimento[i] > 0.0:
            return i
        elif tiposCombustible[i] == '-':
            return i


class ProcesamientoRutas:
    def __init__(self, dataCOESTI, dataExternos):
        self.dataCOESTI = dataCOESTI
        self.dataExternos = dataExternos
        self.direcciones = json.load(open('archivos_json/direcciones.json', encoding='utf8'))
        self.unidades = json.load(open('archivos_json/unidades.json', encoding='utf8'))
        self.combustibles = json.load(open('archivos_json/combustibles.json', encoding='utf8'))

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

    def exportarDetalleCombustiblePorCompartimento(self, rutaSalida, unidades, capacidadCompartimento,
                                                   tiposCombustible):
        # Placa de tracto | Empresa | Capacidad total | Total de compartimentos | Número de compartimento |
        # Capacidad de compartimento | Material | Descripción | Producto | Cantidad suministrada
        unidadesUtilizadas = [unidad for unidad in unidades]
        datos = []
        while len(unidadesUtilizadas) > 0:
            unidad = unidadesUtilizadas[0]
            numeroCompartimentos = self.unidades[unidad]['# Compartimentos']

            # Se extrae datos de la unidad
            capacidadCompartimentoActual = capacidadCompartimento[:numeroCompartimentos]
            tiposCombustibleActual = tiposCombustible[:numeroCompartimentos]

            # Se eliminan los datos de los arrays globales
            del capacidadCompartimento[:numeroCompartimentos]
            del tiposCombustible[:numeroCompartimentos]
            del unidadesUtilizadas[0]

            arrayCompartimentos = self.unidades[unidad]['Compartimentos']

            for i in range(numeroCompartimentos):
                fila = []

                # Se agrega columna de Placa de tracto
                fila.append(unidad)

                # Se agrega columna de Empresa
                fila.append(self.unidades[unidad]['Empresa'])

                # Se agrega columna de Capacidad total
                fila.append(self.unidades[unidad]['Capacidad'])

                # Se agrega columna de Total de compartimentos
                fila.append(self.unidades[unidad]['# Compartimentos'])

                # Se agrega columna de Número de compartimento
                fila.append(i + 1)

                # Se agrega columna de Capacidad de compartimento
                fila.append(arrayCompartimentos[i])

                if str(tiposCombustibleActual[i]) == '-':
                    # Se agrega columna de Material
                    fila.append('Ninguno')

                    # Se agrega columna de Descripción
                    fila.append('Ninguno')

                    # Se agrega columna de Producto
                    fila.append('Ninguno')
                else:
                    # Se agrega columna de Material
                    fila.append(str(tiposCombustibleActual[i]))

                    # Se agrega columna de Descripción
                    fila.append(self.combustibles[str(tiposCombustibleActual[i])]['Descripción'])

                    # Se agrega columna de Producto
                    fila.append(self.combustibles[str(tiposCombustibleActual[i])]['Producto'])

                # Se agrega columna de Cantidad
                fila.append(arrayCompartimentos[i] - capacidadCompartimentoActual[i])

                # Se agrega la fila a los datos
                datos.append(fila)

        # Se crea y exporta el data frame con los datos
        encabezados = ['Placa de tracto', 'Empresa', 'Capacidad total', 'Total de compartimentos',
                       'Número de compartimento', 'Capacidad de compartimento', 'Material', 'Descripción',
                       'Producto', 'Cantidad llenada']
        dataFrameFinal = pd.DataFrame(datos, columns=encabezados)

        # Exportar varias hojas en el mismo archivo Excel
        with pd.ExcelWriter(rutaSalida) as archivoExcel:
            dataFrameFinal.to_excel(archivoExcel, index=True, header=True, sheet_name='Vuelta 1')
            dataFrameFinal.to_excel(archivoExcel, index=True, header=True, sheet_name='Vuelta 2')
            dataFrameFinal.to_excel(archivoExcel, index=True, header=True, sheet_name='Vuelta 3')

    def distribuirUnidades(self, recorridoGlobal):
        recorrido = []
        unidades = []

        capacidadCompartimento = []
        tiposCombustible = []
        unidadesCompartimento = []

        estacionesPorUnidades = {}
        listaUnidades = list(self.unidades.keys())
        for idUnidad in listaUnidades:
            unidad = self.unidades[idUnidad]
            capacidadCompartimento = capacidadCompartimento + unidad['Compartimentos']
            tiposCombustible = tiposCombustible + ['-' for i in range(unidad['# Compartimentos'])]
            unidadesCompartimento = unidadesCompartimento + [idUnidad for i in range(unidad['# Compartimentos'])]
            estacionesPorUnidades[idUnidad] = []

        for estacion in recorridoGlobal:
            # Filtrar pedidos de una estación
            dataFrameEstacion = self.dataCOESTI[self.dataCOESTI['Centro'] == estacion]
            # print(dataFrameEstacion.to_string())

            # Recorrer pedidos de la estación
            for index, row, in dataFrameEstacion.iterrows():
                # Se extrae la cantidad y tipo de combustible al pedido
                pedido = row['Sugerido']
                tipo = row['Material']
                while pedido > 0.0:
                    # Buscar compartimento no lleno del mismo tipo de combustible o uno que esté vacío
                    compartimentoALlenar = buscarSiguienteCompartimento(tipo, capacidadCompartimento, tiposCombustible)

                    # Se asigna el tipo de combustible al compartimento
                    tiposCombustible[compartimentoALlenar] = tipo

                    # Si el pedido alcanza en el compartimento
                    if pedido <= capacidadCompartimento[compartimentoALlenar]:
                        # Se reduce la cantidad del pedido al compartimento
                        capacidadCompartimento[compartimentoALlenar] = \
                            capacidadCompartimento[compartimentoALlenar] - pedido

                        # Se agrega la estación al recorrido de la unidad
                        estacionesPorUnidades[unidadesCompartimento[compartimentoALlenar]].append(estacion)

                        # El pedido queda en cero
                        pedido = pedido - pedido

                    # Si el pedido no alcanza en el compartimento
                    else:
                        # Se resta la capacidad restante del compartimento al pedido
                        pedido = pedido - capacidadCompartimento[compartimentoALlenar]

                        # La capacidad del compartimento queda en cero
                        capacidadCompartimento[compartimentoALlenar] = \
                            capacidadCompartimento[compartimentoALlenar] - capacidadCompartimento[compartimentoALlenar]

                        # Se agrega la estación al recorrido de la unidad
                        estacionesPorUnidades[unidadesCompartimento[compartimentoALlenar]].append(estacion)

        # Se recorren todas las unidades
        for idUnidad in estacionesPorUnidades.keys():
            # Si se tiene al menos una parada en la unidad
            if len(estacionesPorUnidades[idUnidad]) > 0:
                # Se agrega la unidad y el array del recorrido, eliminando los duplicados
                unidades.append(idUnidad)
                recorrido.append(list(dict.fromkeys(estacionesPorUnidades[idUnidad])))

        # Exportar Excel con los tipos de combustibles por compartimento
        self.exportarDetalleCombustiblePorCompartimento('datos_salida/Distribución_Combustibles_Unidades.xlsx',
                                                        unidades, capacidadCompartimento, tiposCombustible)

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

    def exportarRecorridoUnidades(self, rutaSalida, recorrido, unidades):
        # Placa de tracto | Empresa | Capacidad total | # Compartimentos | Orden de llegada | Destinatario |
        # Distrito | Estación | Dirección | Grupo
        datos = []
        for i in range(len(unidades)):
            unidad = unidades[i]
            recorridoActual = recorrido[i]
            for j in range(len(recorridoActual)):
                fila = []
                estacion = recorridoActual[j]

                # Se agrega columna de Placa de tracto
                fila.append(unidad)

                # Se agrega columna de Empresa
                fila.append(self.unidades[unidad]['Empresa'])

                # Se agrega columna de Capacidad total
                fila.append(self.unidades[unidad]['Capacidad'])

                # Se agrega columna de # Compartimentos
                fila.append(self.unidades[unidad]['# Compartimentos'])

                # Se agrega columna de Orden de llegada
                fila.append(j + 1)

                # Se agrega columna de Destinatario
                fila.append(estacion)

                # Se agrega columna de Distrito
                fila.append(self.direcciones[estacion]['Distrito'])

                # Se agrega columna de Estación
                fila.append(self.direcciones[estacion]['Estación'])

                # Se agrega columna de Dirección
                fila.append(self.direcciones[estacion]['Dirección'])

                # Se agrega columna de Grupo
                fila.append(self.direcciones[estacion]['Grupo'])

                # Se agrega la fila a los datos
                datos.append(fila)

        # Se crea y exporta el data frame con los datos
        encabezados = ['Placa de tracto', 'Empresa', 'Capacidad total', '# Compartimentos', 'Orden de llegada',
                       'Destinatario', '# Distrito', 'Estación', 'Dirección', 'Grupo']
        dataFrameFinal = pd.DataFrame(datos, columns=encabezados)

        # Exportar varias hojas en el mismo archivo Excel
        with pd.ExcelWriter(rutaSalida) as archivoExcel:
            dataFrameFinal.to_excel(archivoExcel, index=True, header=True, sheet_name='Vuelta 1')
            dataFrameFinal.to_excel(archivoExcel, index=True, header=True, sheet_name='Vuelta 2')
            dataFrameFinal.to_excel(archivoExcel, index=True, header=True, sheet_name='Vuelta 3')

    def calcularRutas(self, separador, inicio):
        estacionesCOESTI = self.dataCOESTI['Centro'].unique().tolist()
        estacionesExternos = list(map(str, self.dataExternos['Solicitante'].unique().tolist()))
        # estaciones = estacionesCOESTI + estacionesExternos
        estaciones = estacionesCOESTI

        # Se verifica si es que existen las estaciones en el Excel de direcciones
        estacionesExistentes = []
        for estacion in estaciones:
            if estacion in self.direcciones:
                estacionesExistentes.append(estacion)
            else:
                print('Estación:', estacion, 'no encontrada')
        estaciones = estacionesExistentes

        tiempo = '{:.3f}'.format(round(timer() - inicio, 3))
        print(
            '{0: <50}'.format('   2.1. Calculando distancias entre estaciones'),
            separador * 30, '    ', '{0: >7}'.format(tiempo), 'segundos'
        )

        # Construir lista de distancias
        # distanciasEstaciones = []
        # for i in range(len(estaciones)):
        #     for j in range(len(estaciones)):
        #         if i != j:
        #             origen = (
        #                 self.direcciones[estaciones[i]]['Latitud'],
        #                 self.direcciones[estaciones[i]]['Longitud']
        #             )
        #             destino = (
        #                 self.direcciones[estaciones[j]]['Latitud'],
        #                 self.direcciones[estaciones[j]]['Longitud']
        #             )
        #             distancia = geodesic(origen, destino).kilometers
        #             distanciasEstaciones.append((i, j, distancia))

        tiempo = '{:.3f}'.format(round(timer() - inicio, 3))
        print(
            '{0: <50}'.format('   2.2. Construyendo recorrido óptimo'),
            separador * 30, '    ', '{0: >7}'.format(tiempo), 'segundos'
        )

        # # Construir recorrido TSP
        # funcionConveniencia = mlrose.TravellingSales(distances=distanciasEstaciones)
        # ajusteProblema = mlrose.TSPOpt(length=len(estaciones), fitness_fn=funcionConveniencia, maximize=True)
        # posicionesRecorrido, distanciaGlobal = mlrose.genetic_alg(
        #     ajusteProblema, mutation_prob=0.2, max_attempts=100, random_state=2
        # )
        #
        # guardarRutaTSP('datos_intermedios/rutaTSP.txt', posicionesRecorrido, distanciaGlobal)

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
        unidadesOrdenadas = sorted(self.unidades, key=lambda valor: self.unidades[valor]['Capacidad'], reverse=True)
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

        # Exportar rutas de unidades
        self.exportarRecorridoUnidades('datos_salida/Recorrido_Estaciones_Unidades.xlsx', recorrido, unidades)

        return recorrido, unidades
