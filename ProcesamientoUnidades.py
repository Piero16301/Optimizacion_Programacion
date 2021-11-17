import json

import pandas as pd


def cargarExcel(nombreExcel, nombreHoja, encabezado):
    # Lectura inicial archivo Excel
    excel = pd.read_excel(nombreExcel, sheet_name=nombreHoja, header=encabezado)
    dataFrame = pd.DataFrame(excel)

    return dataFrame


class ProcesamientoUnidades:
    def __init__(self, archivoExcel):
        self.rutaExcel = archivoExcel

        self.dataTranscord = pd.DataFrame()
        self.dataLTP = pd.DataFrame()
        self.dataApoyo = pd.DataFrame()

        self.indiceTranscord = {}
        self.indiceLTP = {}
        self.indiceApoyo = {}

    def organizarDataTranscord(self, hojaTranscord):
        dataFrameTranscord = cargarExcel(self.rutaExcel, hojaTranscord, 0)

        # Se seleccionan solo las columnas con datos
        dataFrameTranscord = dataFrameTranscord.iloc[:, 0:65]

        return dataFrameTranscord

    def organizarDataLTP(self, hojaLTP):
        dataFrameLTP = cargarExcel(self.rutaExcel, hojaLTP, 0)

        # Se seleccionan solo las columnas con datos
        dataFrameLTP = dataFrameLTP.iloc[:, 0:50]

        return dataFrameLTP

    def organizarDataApoyo(self, hojaApoyo):
        dataFrameApoyo = cargarExcel(self.rutaExcel, hojaApoyo, 0)

        # Se seleccionan solo las columnas con datos
        dataFrameApoyo = dataFrameApoyo.iloc[:, 0:39]

        return dataFrameApoyo

    def guardarIndice(self, dataFrame, tipo):
        indice = {}
        for index, row, in dataFrame.iterrows():
            placa = row['Placa de Tracto o Camión']
            indice[placa] = {
                'Empresa': row['Nombre de Empresa de Transporte'],
                'Placa Cisterna': row['Placa de Cisterna'],
                'Propietario': row['Unidad Propia o Tercera'],
                'Capacidad': row['Capacidad Cisterna'],
                '# Compartimentos': row['# Compartimentos'],
                'Compartimentos': []
            }

            for i in range(1, 10):
                if pd.notna(row[str(i)]):
                    indice[placa]['Compartimentos'].append(float(row[str(i)]))

            indice[placa]['Capacidad'] = indice[placa]['Capacidad'].replace(' GLS.', '')
            indice[placa]['Capacidad'] = float(indice[placa]['Capacidad'])

        if tipo == 'transcord':
            self.indiceTranscord = indice
            with open('archivos_json/transcord.json', 'w', encoding='utf8') as transcordJSON:
                json.dump(self.indiceTranscord, transcordJSON, indent=4, ensure_ascii=False)
        elif tipo == 'LTP':
            self.indiceLTP = indice
            with open('archivos_json/ltp.json', 'w', encoding='utf8') as ltpJSON:
                json.dump(self.indiceLTP, ltpJSON, indent=4, ensure_ascii=False)
        elif tipo == 'Apoyo':
            self.indiceApoyo = indice
            with open('archivos_json/apoyo.json', 'w', encoding='utf8') as apoyoJSON:
                json.dump(self.indiceApoyo, apoyoJSON, indent=4, ensure_ascii=False)

    def procesarData(self):
        # Procesar data Transcord
        self.dataTranscord = self.organizarDataTranscord('Flota Transcord')
        self.guardarIndice(self.dataTranscord, 'transcord')

        # Procesar data LTP
        self.dataLTP = self.organizarDataLTP('Flota LTP')
        self.guardarIndice(self.dataLTP, 'LTP')

        # Procesar data Apoyo
        self.dataApoyo = self.organizarDataApoyo('Flota Apoyo Translyn')
        self.guardarIndice(self.dataApoyo, 'Apoyo')
