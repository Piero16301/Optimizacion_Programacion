import json
import mlrose
import pandas as pd
import copy

from timeit import default_timer as timer
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
    return -1


class ProcesamientoRutas:
    def __init__(self, dataCOESTI, dataExternos):
        self.dataCOESTI = dataCOESTI
        self.dataExternos = dataExternos
        self.direcciones = json.load(open('archivos_json/direcciones.json', encoding='utf8'))
        self.unidades = json.load(open('archivos_json/unidades.json', encoding='utf8'))
        self.combustibles = json.load(open('archivos_json/combustibles.json', encoding='utf8'))

        self.recorridoGlobal = []

        self.vueltas = {}

    def optimizacionRutaMayor(self):
        maximaDistancia = 0
        indiceMaximo = 0

        for i in range(len(self.recorridoGlobal)):
            if i == len(self.recorridoGlobal) - 1:
                origen = (
                    self.direcciones[self.recorridoGlobal[i]]['Latitud'],
                    self.direcciones[self.recorridoGlobal[i]]['Longitud']
                )
                destino = (
                    self.direcciones[self.recorridoGlobal[0]]['Latitud'],
                    self.direcciones[self.recorridoGlobal[0]]['Longitud']
                )
            else:
                origen = (
                    self.direcciones[self.recorridoGlobal[i]]['Latitud'],
                    self.direcciones[self.recorridoGlobal[i]]['Longitud']
                )
                destino = (
                    self.direcciones[self.recorridoGlobal[i + 1]]['Latitud'],
                    self.direcciones[self.recorridoGlobal[i + 1]]['Longitud']
                )

            if geodesic(origen, destino).kilometers > maximaDistancia:
                maximaDistancia = geodesic(origen, destino).kilometers
                indiceMaximo = i

        if indiceMaximo != (len(self.recorridoGlobal) - 1):
            nuevoRecorridoGlobal = []
            for i in range(indiceMaximo + 1, len(self.recorridoGlobal)):
                nuevoRecorridoGlobal.append(self.recorridoGlobal[i])

            for i in range(indiceMaximo + 1):
                nuevoRecorridoGlobal.append(self.recorridoGlobal[i])

            return nuevoRecorridoGlobal
        else:
            return self.recorridoGlobal

    def distribuirUnidades(self):
        capacidadCompartimento = []
        tiposCombustible = []
        unidadesCompartimento = []

        estacionesPorUnidades = {}

        listaUnidades = list(self.unidades.keys())
        for idUnidad in listaUnidades:
            unidad = self.unidades[idUnidad]
            capacidadCompartimento = capacidadCompartimento + unidad['Compartimentos']
            tiposCombustible = tiposCombustible + ['-' for _ in range(unidad['# Compartimentos'])]
            unidadesCompartimento = unidadesCompartimento + [idUnidad for _ in range(unidad['# Compartimentos'])]
            estacionesPorUnidades[idUnidad] = []

        totalEstacionesIniciales = len(self.recorridoGlobal)
        for _ in range(totalEstacionesIniciales):
            # Copias de los arrays iniciales
            capacidadCompartimentoTemporal = list(capacidadCompartimento)
            tiposCombustibleTemporal = list(tiposCombustible)
            unidadesCompartimentoTemporal = list(unidadesCompartimento)

            estacionesPorUnidadesTemporal = copy.deepcopy(estacionesPorUnidades)

            # Filtrar pedidos de una estación
            dataFrameEstacion = self.dataCOESTI[self.dataCOESTI['Destinatario'] == self.recorridoGlobal[0]]

            # Recorrer pedidos de la estación
            for index, row, in dataFrameEstacion.iterrows():
                # Se extrae la cantidad y tipo de combustible al pedido
                pedido = row['Cant. entrega']
                tipo = row['Producto']
                while pedido > 0.0:
                    # Buscar compartimento no lleno del mismo tipo de combustible o uno que esté vacío
                    compartimentoALlenar = buscarSiguienteCompartimento(
                        tipo, capacidadCompartimentoTemporal, tiposCombustibleTemporal
                    )

                    # Cuando la flota ya está llena (cambio de vuelta)
                    if compartimentoALlenar == -1:
                        numeroVuelta = 'Vuelta ' + str(len(self.vueltas) + 1)
                        self.vueltas[numeroVuelta] = {
                            'Capacidad de Compartimento': capacidadCompartimento,
                            'Tipos de Combustible': tiposCombustible,
                            'Unidades de Compartimento': unidadesCompartimento,
                            'Estaciones por Unidades': {
                                key: list(dict.fromkeys(estacionesPorUnidades[key])) for key in estacionesPorUnidades
                            }
                        }
                        return False

                    # Se asigna el tipo de combustible al compartimento
                    tiposCombustibleTemporal[compartimentoALlenar] = tipo

                    # Si el pedido alcanza en el compartimento
                    if pedido <= capacidadCompartimentoTemporal[compartimentoALlenar]:
                        # Se reduce la cantidad del pedido al compartimento
                        capacidadCompartimentoTemporal[compartimentoALlenar] = \
                            capacidadCompartimentoTemporal[compartimentoALlenar] - pedido

                        # Se agrega la estación al recorrido de la unidad
                        estacionesPorUnidadesTemporal[unidadesCompartimentoTemporal[compartimentoALlenar]].append(
                            self.recorridoGlobal[0]
                        )

                        # El pedido queda en cero
                        pedido = pedido - pedido

                    # Si el pedido no alcanza en el compartimento
                    else:
                        # Se resta la capacidad restante del compartimento al pedido
                        pedido = pedido - capacidadCompartimentoTemporal[compartimentoALlenar]

                        # La capacidad del compartimento queda en cero
                        capacidadCompartimentoTemporal[compartimentoALlenar] = \
                            capacidadCompartimentoTemporal[compartimentoALlenar] -\
                            capacidadCompartimentoTemporal[compartimentoALlenar]

                        # Se agrega la estación al recorrido de la unidad
                        estacionesPorUnidadesTemporal[unidadesCompartimentoTemporal[compartimentoALlenar]].append(
                            self.recorridoGlobal[0]
                        )

            # Se copia a los arrays principales si se ha despachado con éxito todos los pedidos de la estación
            capacidadCompartimento = list(capacidadCompartimentoTemporal)
            tiposCombustible = list(tiposCombustibleTemporal)
            unidadesCompartimento = list(unidadesCompartimentoTemporal)

            estacionesPorUnidades = copy.deepcopy(estacionesPorUnidadesTemporal)

            # Se elimina la estación abastecida
            self.recorridoGlobal.remove(self.recorridoGlobal[0])

        # Todos los pedidos fueron abastecidos en esta vuelta
        numeroVuelta = 'Vuelta ' + str(len(self.vueltas) + 1)
        self.vueltas[numeroVuelta] = {
            'Capacidad de Compartimento': capacidadCompartimento,
            'Tipos de Combustible': tiposCombustible,
            'Unidades de Compartimento': unidadesCompartimento,
            'Estaciones por Unidades': {
                key: list(dict.fromkeys(estacionesPorUnidades[key])) for key in estacionesPorUnidades
            }
        }
        return True

    def optimizarRutasUnidades(self):
        for vuelta in self.vueltas:
            estacionesVueltaActual = self.vueltas[vuelta]['Estaciones por Unidades']
            for unidad in estacionesVueltaActual:
                recorrido = estacionesVueltaActual[unidad]
                if len(recorrido) > 2:
                    recorridoActual = recorrido
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

                        self.vueltas[vuelta]['Estaciones por Unidades'][unidad] = list(nuevoRecorridoActual)

    def exportarDetalleCombustiblePorCompartimento(self, rutaSalida):
        # Placa de tracto | Empresa | Capacidad total | Total de compartimentos | Número de compartimento |
        # Capacidad de compartimento | Material | Descripción | Producto | Cantidad suministrada

        # Array con un Data Frame por vuelta
        dataFrames = []

        # Iteración sobre el número de vueltas
        for vuelta in self.vueltas:
            unidades = []

            for unidad in self.vueltas[vuelta]['Estaciones por Unidades']:
                if len(self.vueltas[vuelta]['Estaciones por Unidades'][unidad]) > 0:
                    unidades.append(unidad)

            capacidadCompartimento = list(self.vueltas[vuelta]['Capacidad de Compartimento'])
            tiposCombustible = list(self.vueltas[vuelta]['Tipos de Combustible'])

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
            dataFrameVuelta = pd.DataFrame(datos, columns=encabezados)

            dataFrames.append(dataFrameVuelta)

        # Exportar varias hojas en el mismo archivo Excel
        with pd.ExcelWriter(rutaSalida) as archivoExcel:
            for i in range(len(dataFrames)):
                nombreHoja = 'Vuelta ' + str(i + 1)
                dataFrames[i].to_excel(archivoExcel, index=False, header=True, sheet_name=nombreHoja)

    def exportarRecorridoUnidades(self, rutaSalida):
        # Placa de tracto | Empresa | Capacidad total | # Compartimentos | Orden de llegada | Destinatario |
        # Distrito | Estación | Dirección | Grupo

        # Array con un Data Frame por vuelta
        dataFrames = []

        # Iteración sobre el número de vueltas
        for vuelta in self.vueltas:
            recorrido = []
            unidades = []
            for unidad in self.vueltas[vuelta]['Estaciones por Unidades']:
                if len(self.vueltas[vuelta]['Estaciones por Unidades'][unidad]) > 0:
                    recorrido.append(self.vueltas[vuelta]['Estaciones por Unidades'][unidad])
                    unidades.append(unidad)

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
            dataFrameVuelta = pd.DataFrame(datos, columns=encabezados)

            dataFrames.append(dataFrameVuelta)

        # Exportar varias hojas en el mismo archivo Excel
        with pd.ExcelWriter(rutaSalida) as archivoExcel:
            for i in range(len(dataFrames)):
                nombreHoja = 'Vuelta ' + str(i + 1)
                dataFrames[i].to_excel(archivoExcel, index=False, header=True, sheet_name=nombreHoja)

    def exportarVueltas(self):
        with open('archivos_json/vueltas.json', 'w', encoding='utf8') as vueltasJSON:
            json.dump(self.vueltas, vueltasJSON, indent=4, ensure_ascii=False)

    def calcularRutas(self, separador, inicio, maximosIntentosRecorrido):
        estacionesCOESTI = self.dataCOESTI['Destinatario'].unique().tolist()
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
            '{0: <60}'.format('   2.1. Calculando distancias entre estaciones'),
            separador * 30, '    ', '{0: >7}'.format(tiempo), 'segundos'
        )

        # # Construir lista de distancias
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
            '{0: <60}'.format('   2.2. Construyendo recorrido óptimo'),
            separador * 30, '    ', '{0: >7}'.format(tiempo), 'segundos'
        )

        # # Construir recorrido TSP
        # funcionConveniencia = mlrose.TravellingSales(distances=distanciasEstaciones)
        # ajusteProblema = mlrose.TSPOpt(length=len(estaciones), fitness_fn=funcionConveniencia, maximize=True)
        #
        # if maximosIntentosRecorrido:
        #     posicionesRecorrido, distanciaGlobal = mlrose.genetic_alg(
        #         ajusteProblema, mutation_prob=0.2, max_attempts=100, random_state=2
        #     )
        # else:
        #     posicionesRecorrido, distanciaGlobal = mlrose.genetic_alg(
        #         ajusteProblema, random_state=2
        #     )
        #
        # guardarRutaTSP('datos_intermedios/rutaTSP.txt', posicionesRecorrido, distanciaGlobal)

        posicionesRecorrido, distanciaGlobal = cargarRutaTSP('datos_intermedios/rutaTSP.txt')

        stringDistanciaTotal = '        2.2.1. Distancia total: ' + str(round(distanciaGlobal, 3)) + ' Km'
        tiempo = '{:.3f}'.format(round(timer() - inicio, 3))
        print(
            '{0: <60}'.format(stringDistanciaTotal),
            separador * 30, '    ', '{0: >7}'.format(tiempo), 'segundos'
        )

        # Convertir posiciones a codigos de estación
        for i in range(len(posicionesRecorrido)):
            self.recorridoGlobal.append(estaciones[posicionesRecorrido[i]])

        self.recorridoGlobal = self.optimizacionRutaMayor()

        tiempo = '{:.3f}'.format(round(timer() - inicio, 3))
        print(
            '{0: <60}'.format('   2.3. Ordenando unidades'),
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
            '{0: <60}'.format('   2.4. Distribuyendo unidades'),
            separador * 30, '    ', '{0: >7}'.format(tiempo), 'segundos'
        )

        # Procesar el número de vueltas y su optimización
        todosPedidosCompletados = False
        while not todosPedidosCompletados:
            # Se sigue llamando a la función hasta que se despachen todos los pedidos
            todosPedidosCompletados = self.distribuirUnidades()

        # Optimizar rutas individuales
        self.optimizarRutasUnidades()

        # Exportar archivos de distribución de compartimentos y recorrido de estaciones
        self.exportarDetalleCombustiblePorCompartimento('datos_salida/Distribución_Combustibles_Unidades.xlsx')
        self.exportarRecorridoUnidades('datos_salida/Recorrido_Estaciones_Unidades.xlsx')

        # Exportar JSON de las vueltas
        self.exportarVueltas()
