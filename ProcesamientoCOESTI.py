import pandas as pd
import json


def cargarExcel(nombreExcel, encabezado):
    # Lectura inicial archivo Excel
    excel = pd.read_excel(nombreExcel, header=encabezado)
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
        self.combustibles = json.load(open('archivos_json/combustibles.json', encoding='utf8'))
        self.terminales = json.load(open('archivos_json/terminales.json', encoding='utf8'))

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

    def seleccionarColumnas(self):
        datos = []
        for index, row, in self.dataFrame.iterrows():
            fila = []

            fila.append(row['Destinatario'])
            fila.append(self.direcciones[row['Destinatario']]['Estación'])
            fila.append(self.direcciones[row['Destinatario']]['Dirección'])
            fila.append(self.direcciones[row['Destinatario']]['Distrito'])
            fila.append(self.direcciones[row['Destinatario']]['Población'])
            fila.append(self.direcciones[row['Destinatario']]['Zona'])
            fila.append(row['Cant. entrega'])
            fila.append(str(row['Producto']))
            fila.append(self.combustibles[str(row['Producto'])]['Descripción'])
            fila.append(row['Centro carga'])
            fila.append(self.terminales[row['Centro carga']]['Nombre'])

            datos.append(fila)

        encabezados = ['Código de estación', 'Nombre de estación', 'Dirección', 'Distrito', 'Población', 'Zona',
                       'Cantidad de entrega', 'Producto', 'Descripción', 'Código de centro de carga',
                       'Nombre de centro de carga']

        return pd.DataFrame(datos, columns=encabezados)

    def procesarData(self):
        # Organizar data del Excel Inicial
        self.dataFrame = cargarExcel(self.rutaExcel, 0)

        # Aplicar filtros
        self.dataFrame = self.aplicarFiltros()

        # Seleccionar columnas que se van a utilizar
        self.dataFrame = self.seleccionarColumnas()

        # Guardar como Excel
        guardarExcel(self.dataFrame, 'datos_intermedios/Data_Filtrada_COESTI.xlsx', False, True)

        # Carga de datos desde Excel
        self.dataFrame = cargarExcel('datos_intermedios/Data_Filtrada_COESTI.xlsx', 0)
