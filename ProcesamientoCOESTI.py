import pandas as pd
import json


def cargarExcel(nombreExcel, nombreHoja, encabezado):
    # Lectura inicial archivo Excel
    excel = pd.read_excel(nombreExcel, sheet_name=nombreHoja, header=encabezado)
    dataFrame = pd.DataFrame(excel)

    return dataFrame


def guardarExcel(dataFrame, nombreExcel, index, header):
    # Guardar como Excel
    dataFrame.to_excel(nombreExcel, index=index, header=header, sheet_name='Hoja 1')


class ProcesamientoCOESTI:
    def __init__(self, archivoExcel):
        self.rutaExcel = archivoExcel
        self.dataFrame = pd.DataFrame()
        self.direcciones = json.load(open('archivos_json/direcciones.json', encoding='utf8'))

    def aplicarFiltros(self):
        # Filtro de filas de empresa COESTI
        dataFiltroEmpresa = self.dataFrame[self.dataFrame['Nombre Of.Ventas 1'] == 'COESTI']

        # Filtro de filas de región Callao (07)
        dataFiltroRegionCallao = dataFiltroEmpresa[dataFiltroEmpresa['Región'] == 7]

        # Filtro de filas de región Lima (15)
        dataFiltroRegionLima = dataFiltroEmpresa[dataFiltroEmpresa['Región'] == 15]

        filtrosRegiones = [dataFiltroRegionCallao, dataFiltroRegionLima]
        dataFiltroRegion = pd.concat(filtrosRegiones)

        # Reiniciar los índices de las filas
        indicesReiniciados = dataFiltroRegion.reset_index(drop=True)

        return indicesReiniciados

    def procesarData(self):
        # Organizar data del Excel Inicial
        self.dataFrame = cargarExcel(self.rutaExcel, 'SEM47', 0)

        # Aplicar filtros
        self.dataFrame = self.aplicarFiltros()

        # Guardar como Excel
        guardarExcel(self.dataFrame, 'datos_intermedios/Data_Filtrada_COESTI.xlsx', False, True)

        # Carga de datos desde Excel
        self.dataFrame = cargarExcel('datos_intermedios/Data_Filtrada_COESTI.xlsx', 'Hoja 1', 0)
