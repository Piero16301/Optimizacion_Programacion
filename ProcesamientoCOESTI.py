import pandas as pd

from ConvertidorLocalizacion import ConvertidorLocalizacion


def cargarExcel(nombreExcel, nombreHoja, encabezado):
    # Lectura inicial archivo Excel
    excel = pd.read_excel(nombreExcel, sheet_name=nombreHoja, header=encabezado)
    dataFrame = pd.DataFrame(excel)

    return dataFrame


def guardarExcel(dataFrame, nombreExcel, index, header):
    # Guardar como Excel
    dataFrame.to_excel(nombreExcel, index=index, header=header)


class ProcesamientoCOESTI:
    def __init__(self, archivoExcel):
        self.rutaExcel = archivoExcel
        self.dataFrame = pd.DataFrame()

    def organizarData(self, hoja):
        # Lectura inicial archivo Excel de COESTI
        dataFrameInicial = cargarExcel(self.rutaExcel, hoja, None)

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

    def aplicarFiltros(self):
        # Filtro de filas de zona Lima
        dataFiltroZona = self.dataFrame[self.dataFrame['Zona'] == 'LIMA']

        # Filtro de filas con cantidad sugerida diferente de nulo
        dataFiltroSugerido = dataFiltroZona[dataFiltroZona['Sugerido'].notna()]

        # Reiniciar los índices de las filas
        indicesReiniciados = dataFiltroSugerido.reset_index(drop=True)

        return indicesReiniciados

    def preProcesarData(self):
        """
        # Organizar data del Excel Inicial
        print('Leyendo data de COESTI...')
        self.dataFrame = self.organizarData('CL')

        # Aplicar filtros
        print('Aplicando filtros...')
        self.dataFrame = self.aplicarFiltros()
        # print(self.dataFrame.to_string())

        # Guardar como Excel
        print('Guardando data filtrada...')
        guardarExcel(self.dataFrame, 'datos_intermedios/Data_Formateada_COESTI.xlsx', False, True)

        # Carga de datos desde Excel
        print('Cargando data filtrada...')
        self.dataFrame = cargarExcel('datos_intermedios/Data_Formateada_COESTI.xlsx', 'Sheet1', 0)

        # Columnas seleccionadas => Centro, Distrito, Estación, Material, Descripción, Producto, Sugerido
        print('Seleccionando columnas...')
        self.dataFrame = self.dataFrame.iloc[:, [0, 6, 7, 8, 9, 10, 29]]
        # print(columnasImportantes.to_string(), "\n")

        # Lista de tipos de combustible
        tiposCombustible = ['G90', 'G95', 'G97', 'Diesel']
        totalCombustible = []

        print('Calculando cantidad total de productos...')
        for tipo in tiposCombustible:
            totalCombustible.append(self.dataFrame[self.dataFrame['Producto'] == tipo]['Sugerido'].sum())
            print('Cantidad', tipo + ':', totalCombustible[-1])

        # Cantidad total de COESTI
        totalCoesti = sum(totalCombustible)
        print('\nTotal COESTI:', totalCoesti, '\n')

        # Listas de direcciones, latitudes y longitudes
        direcciones = []
        latitudes = []
        longitudes = []

        convertidorLocalizacion = ConvertidorLocalizacion()

        print('Calculando localización de estaciones...')
        # Obtención de coordenadas
        for index, row, in self.dataFrame.iterrows():
            direccion = 'Gasolinera Primax ' + row['Estación'] + ' ' + row['Distrito'] + ' Perú'
            direccionFormal, latitud, longitud = convertidorLocalizacion.convertirDireccionACoordenadas(
                row['Centro'],
                direccion
            )
            direcciones.append(direccionFormal)
            latitudes.append(latitud)
            longitudes.append(longitud)

        # Agregar columnas de direccion, latitud y longitud al dataframe
        self.dataFrame.insert(7, 'Dirección', direcciones, True)
        self.dataFrame.insert(8, 'Latitud', latitudes, True)
        self.dataFrame.insert(9, 'Longitud', longitudes, True)

        # print(self.dataFrame.to_string())

        # Guardar como Excel
        print('Guardando data de localización...')
        guardarExcel(self.dataFrame, 'datos_intermedios/Data_Direcciones_COESTI.xlsx', False, True)
        """

        # Carga de datos desde Excel
        print('Cargando data de localización...')
        self.dataFrame = cargarExcel('datos_intermedios/Data_Direcciones_COESTI.xlsx', 'Sheet1', 0)
