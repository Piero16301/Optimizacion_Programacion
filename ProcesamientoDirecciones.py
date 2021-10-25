import pandas as pd
import json


def cargarExcel(nombreExcel, nombreHoja, encabezado):
    # Lectura inicial archivo Excel
    excel = pd.read_excel(nombreExcel, sheet_name=nombreHoja, header=encabezado)
    dataFrame = pd.DataFrame(excel)

    return dataFrame


class ProcesamientoDirecciones:
    def __init__(self, archivoExcel):
        self.rutaExcel = archivoExcel
        self.dataFrame = pd.DataFrame()
        self.direcciones = {}

    def procesarData(self):
        # Organizar data del Excel Inicial
        print('Leyendo data de Direcciones...')
        self.dataFrame = cargarExcel(self.rutaExcel, 'Lima', 0)

        # Se crea un diccionario con los campos importantes de ubicación
        for index, row, in self.dataFrame.iterrows():
            self.direcciones[row['Destinatario']] = {
                'Estación':  row['Cliente'],
                'Zona':      row['Zona'],
                'Distrito':  row['Distrito'],
                'Población': row['Población'],
                'Dirección': row['Dirección'],
                'Asesor':    row['Asesor Comercial'],
                'Grupo':     row['Grupo de Clientes'],
                'Latitud':   row['Latitud'],
                'Longitud':  row['Longitud'],
                'Símbolo':   row['Símbolo']
            }

        with open('direcciones.json', 'w', encoding='utf8') as direccionesJSON:
            json.dump(self.direcciones, direccionesJSON, indent=4, ensure_ascii=False)
