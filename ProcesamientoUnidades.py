import json

import pandas as pd


def cargarExcel(nombreExcel, nombreHoja, encabezado, indice):
    # Lectura inicial archivo Excel
    excel = pd.read_excel(nombreExcel, sheet_name=nombreHoja, header=encabezado, index_col=indice)
    dataFrame = pd.DataFrame(excel)

    return dataFrame


class ProcesamientoUnidades:
    def __init__(self, archivoExcel):
        self.rutaExcel = archivoExcel

        self.dataUnidades = pd.DataFrame()

        self.indiceUnidades = {}

    def organizarDataUnidades(self, hojaUnidades):
        dataFrameUnidades = cargarExcel(self.rutaExcel, hojaUnidades, 0, 0)

        return dataFrameUnidades

    def guardarIndice(self, dataFrame):
        indice = {}
        for index, row, in dataFrame.iterrows():
            placa = row['Placa de tracto']
            indice[placa] = {
                'Flota': row['Flota'],
                'Empresa': row['Empresa'],
                'Placa de cisterna': row['Placa de cisterna'],
                'Propietario': row['Propietario'],
                'Capacidad': float(row['Capacidad']),
                '# Compartimentos': row['# Compartimentos'],
                'Compartimentos': []
            }

            for i in range(1, 10):
                if pd.notna(row[str(i)]):
                    indice[placa]['Compartimentos'].append(float(row[str(i)]))

        self.indiceUnidades = indice
        with open('archivos_json/unidades.json', 'w', encoding='utf8') as unidadesJSON:
            json.dump(self.indiceUnidades, unidadesJSON, indent=4, ensure_ascii=False)

    def procesarData(self):
        # Procesar data Transcord
        self.dataUnidades = self.organizarDataUnidades('Hoja 1')
        self.guardarIndice(self.dataUnidades)
