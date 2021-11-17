import pandas as pd
import json


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
        self.direcciones = json.load(open('archivos_json/direcciones.json', encoding='utf8'))

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

    def procesarData(self):
        """
        # Organizar data del Excel Inicial
        self.dataFrame = self.organizarData('CL')

        # Aplicar filtros
        self.dataFrame = self.aplicarFiltros()

        # Guardar como Excel
        guardarExcel(self.dataFrame, 'datos_intermedios/Data_Formateada_COESTI.xlsx', False, True)

        # Carga de datos desde Excel
        self.dataFrame = cargarExcel('datos_intermedios/Data_Formateada_COESTI.xlsx', 'Sheet1', 0)

        # Columnas seleccionadas => Centro, Distrito, Estación, Material, Descripción, Producto, Sugerido
        self.dataFrame = self.dataFrame.iloc[:, [0, 6, 7, 8, 9, 10, 29]]

        # Listas de direcciones, latitudes y longitudes
        direcciones = []
        latitudes = []
        longitudes = []

        # Obtención de dirección y coordenadas
        for index, row, in self.dataFrame.iterrows():
            if row['Centro'] in self.direcciones:
                dataEstacion = self.direcciones[row['Centro']]
                direcciones.append(dataEstacion['Dirección'])
                latitudes.append(dataEstacion['Latitud'])
                longitudes.append(dataEstacion['Longitud'])
            else:
                print('Estación no mapeada')
                direcciones.append('---')
                latitudes.append(0.0)
                longitudes.append(0.0)

        # Agregar columnas de direccion, latitud y longitud al dataframe
        self.dataFrame.insert(7, 'Dirección', direcciones, True)
        self.dataFrame.insert(8, 'Latitud', latitudes, True)
        self.dataFrame.insert(9, 'Longitud', longitudes, True)

        # Guardar como Excel
        guardarExcel(self.dataFrame, 'datos_intermedios/Data_Direcciones_COESTI.xlsx', False, True)
        """

        # Carga de datos desde Excel
        self.dataFrame = cargarExcel('datos_intermedios/Data_Direcciones_COESTI.xlsx', 'Sheet1', 0)
