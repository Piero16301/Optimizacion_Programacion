import pandas as pd

from ConvertidorLocalizacion import ConvertidorLocalizacion


class PreProcesamientoCOESTI:
    def __init__(self, archivoExcel):
        self.rutaExcel = archivoExcel
        self.dataFrame = pd.DataFrame()

    def cargarExcel(self, nombreExcel, nombreHoja, encabezado):
        # Lectura inicial archivo Excel
        excel = pd.read_excel(nombreExcel, sheet_name=nombreHoja, header=encabezado)
        dataFrame = pd.DataFrame(excel)

        return dataFrame

    def organizarData(self, dataCOESTI):
        # Lectura inicial archivo Excel de COESTI
        dataFrameInicial = self.cargarExcel(dataCOESTI, 'CL', None)

        # Se eliminan filas y columnas no necesarias
        filtroFilas = dataFrameInicial.iloc[:, 1:37]
        nombresColumnas = ['Centro', 'JOP', 'GOP', 'Transportes', 'Zona', 'Departamento', 'Distrito', 'Estación',
                           'Material', 'Descripción', 'Producto', 'Concatenado', 'Capacidad DGH',
                           'Inventario Max Deseado',
                           'Muerto', 'Varilla', 'Descarga', 'Stock Operativo', 'VTA Promedio Emergencia', 'X 1', 'X 2',
                           'VTA Promedio %', 'VTA Día 04', 'VTA Día 05', 'Incremento VTA', 'Días Stock Emergencia',
                           'VTA Normal', 'Días Stock Normal', 'Pedido', 'Sugerido', 'Días Stock 1', 'Días Stock 2',
                           'Y 1',
                           'Cantidad Aproximada Carga', 'Observación', 'Z 1']

        # Asignación de encabezados de todas las columnas
        dataFrameEncabezado = pd.DataFrame(filtroFilas)
        dataFrameEncabezado.columns = nombresColumnas

        return dataFrameEncabezado

    def aplicarFiltros(self, dataFrameEncabezado):
        # Filtro de filas de zona Lima
        dataFiltroZona = dataFrameEncabezado[dataFrameEncabezado['Zona'] == 'LIMA']

        # Filtro de filas con cantidad sugerida diferente de nulo
        dataFiltroSugerido = dataFiltroZona[dataFiltroZona['Sugerido'].notna()]

        # Reiniciar los índices de las filas
        indicesReiniciados = dataFiltroSugerido.reset_index(drop=True)

        return indicesReiniciados

    def guardarExcel(self, dataFrame, nombreExcel, index, header):
        # Guardar como Excel
        dataFrame.to_excel(nombreExcel, index=index, header=header)

    def preProcesarData(self):
        # Organizar data del Excel Inicial
        # dataFrameEncabezado = organizarData('Data_COESTI.xlsx')

        # Aplicar filtros
        # indicesReiniciados = aplicarFiltros(dataFrameEncabezado)

        # Guardar como Excel
        # guardarExcel(indicesReiniciados, 'Data_Formateada.xlsx')

        # Carga de datos desde Excel
        indicesReiniciados = self.cargarExcel('Data_Formateada.xlsx', 'Sheet1', 0)

        # Columnas seleccionadas => Centro, Distrito, Estación, Material, Descripción, Producto, Sugerido
        columnasImportantes = indicesReiniciados.iloc[:, [0, 6, 7, 8, 9, 10, 29]]
        # print(columnasImportantes.to_string(), "\n")

        # Lista de tipos de combustible
        tiposCombustible = ['G90', 'G95', 'G97', 'Diesel']
        totalCombustible = []

        for tipo in tiposCombustible:
            totalCombustible.append(columnasImportantes[columnasImportantes['Producto'] == tipo]['Sugerido'].sum())
            print('Cantidad', tipo + ':', totalCombustible[-1])

        # Cantidad total de COESTI
        totalCoesti = sum(totalCombustible)
        print('Total COESTI:', totalCoesti, '\n')

        # Listas de direcciones, latitudes y longitudes
        direcciones = []
        latitudes = []
        longitudes = []

        convertidorLocalizacion = ConvertidorLocalizacion()

        # Obtención de coordenadas
        for index, row, in columnasImportantes.iterrows():
            direccion = 'Gasolinera Primax ' + row['Estación'] + ' ' + row['Distrito']
            direccionFormal, latitud, longitud = convertidorLocalizacion.convertirDireccionACoordenadas(
                row['Centro'],
                direccion
            )
            direcciones.append(direccionFormal)
            latitudes.append(latitud)
            longitudes.append(longitud)

        # Agregar columnas de direccion, latitud y longitud al dataframe
        columnasImportantes.insert(7, 'Dirección', direcciones, True)
        columnasImportantes.insert(8, 'Latitud', latitudes, True)
        columnasImportantes.insert(9, 'Longitud', longitudes, True)

        print(columnasImportantes.to_string())

        # Guardar como Excel
        # guardarExcel(columnasImportantes, 'Data_Direcciones.xlsx', False, True)
