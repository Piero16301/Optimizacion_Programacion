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


class ProcesamientoRestricciones:
    def __init__(self, archivoExcel):
        self.rutaExcel = archivoExcel
        self.dataFrame = pd.DataFrame()

        self.direcciones = json.load(open('archivos_json/direcciones.json', encoding='utf8'))

    def seleccionarColumnas(self):
        datos = []
        for index, row, in self.dataFrame.iterrows():
            if str(row['Destinatario']) in self.direcciones:
                fila = []

                fila.append(str(row['Destinatario']))
                fila.append(self.direcciones[str(row['Destinatario'])]['Estación'])
                fila.append(self.direcciones[str(row['Destinatario'])]['Zona'])
                fila.append(self.direcciones[str(row['Destinatario'])]['Distrito'])
                fila.append(self.direcciones[str(row['Destinatario'])]['Población'])
                fila.append(row['TURNOS ATENCIÓN'])
                fila.append(row['TAMAÑO UNIDAD'])

                datos.append(fila)

        encabezados = ['Código de estación', 'Nombre de estación', 'Zona', 'Distrito', 'Población', 'Turno de atención',
                       'Tamaño de unidad']

        return pd.DataFrame(datos, columns=encabezados)

    def procesarData(self):
        # Cargar data del Excel inicial
        self.dataFrame = cargarExcel(self.rutaExcel, 0)

        # Seleccionar columnas que se van a utilizar
        self.dataFrame = self.seleccionarColumnas()

        # Guardar como Excel
        guardarExcel(self.dataFrame, 'datos_intermedios/Data_Filtrada_Restricciones.xlsx', False, True)

        # # Carga de datos desde Excel
        # self.dataFrame = cargarExcel('datos_intermedios/Data_Filtrada_COESTI.xlsx', 0)
