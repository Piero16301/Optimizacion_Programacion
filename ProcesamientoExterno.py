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


class ProcesamientoExterno:
    def __init__(self, archivoExcel):
        self.rutaExcel = archivoExcel
        self.dataFrame = pd.DataFrame()

        self.direcciones = json.load(open('archivos_json/direcciones.json', encoding='utf8'))
        self.combustibles = json.load(open('archivos_json/combustibles.json', encoding='utf8'))
        self.terminales = json.load(open('archivos_json/terminales.json', encoding='utf8'))

    def seleccionarColumnas(self):
        datos = []
        for index, row, in self.dataFrame.iterrows():
            if str(row['Solicitante']) in self.direcciones:
                fila = []

                fila.append(str(row['Solicitante']))
                fila.append(self.direcciones[str(row['Solicitante'])]['Estación'])
                fila.append(self.direcciones[str(row['Solicitante'])]['Dirección'])
                fila.append(self.direcciones[str(row['Solicitante'])]['Distrito'])
                fila.append(self.direcciones[str(row['Solicitante'])]['Población'])
                fila.append(self.direcciones[str(row['Solicitante'])]['Zona'])
                fila.append(row['Cantidad de pedido'])
                fila.append(str(row['Material']))
                fila.append(self.combustibles[str(row['Material'])]['Descripción'])
                fila.append(row['Centro'])
                fila.append(self.terminales[row['Centro']]['Nombre'])

                datos.append(fila)

        encabezados = ['Código de estación', 'Nombre de estación', 'Dirección', 'Distrito', 'Población', 'Zona',
                       'Cantidad de entrega', 'Producto', 'Descripción', 'Código de centro de carga',
                       'Nombre de centro de carga']

        return pd.DataFrame(datos, columns=encabezados)

    def procesarData(self):
        # Cargar Excel inicial
        self.dataFrame = cargarExcel(self.rutaExcel, 0)

        # Seleccionar columnas que se van a utilizar
        self.dataFrame = self.seleccionarColumnas()

        # Guardar como Excel
        guardarExcel(self.dataFrame, 'datos_intermedios/Data_Filtrada_Externos.xlsx', False, True)

        # # Carga de datos desde Excel
        # self.dataFrame = cargarExcel('datos_intermedios/Data_Filtrada_Externos.xlsx', 0)
