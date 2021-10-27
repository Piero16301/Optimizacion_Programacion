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
        dataFrameTranscord = cargarExcel(self.rutaExcel, hojaTranscord, None)

        # Se seleccionan solo las columnas con datos
        dataFrameTranscord = dataFrameTranscord.iloc[:, 0:65]

        # Se establece el nombre de las columnas
        nombresColumnas = ['Región', 'Nombre de Empresa de Transporte', 'Nombre Cliente/Destino',
                           'Plan de Contigencia Aprobado', 'Producto', 'Operación', 'Tipo de Vehículo',
                           'Placa de Tracto o Camión', 'Placa de Cisterna', 'Unidad Propia o Tercera', 'Marca Tracto',
                           'Modelo Tracto', 'Año Fabricación Tracto', 'Marca Cisterna', 'Modelo Cisterna',
                           'Año Fabricación Cisterna', 'Capacidad Cisterna', '# Compartimentos', '1', '2', '3', '4',
                           '5', '6', '7', '8', '9', 'Vencimiento de Tarjeta de Circulación Tracto',
                           'Vencimiento de Tarjeta de Circulación Cisterna', 'Empresa de Cubicación',
                           'Nro. de Tarjeta de Cubicación', 'Vencimiento de Cubicación', 'Tabla de Aforo',
                           'Sello INACAL', 'Tapas Manhole Soldadas', 'Scully y Valvulas de Fondo',
                           'Fecha Vencimiento SOAT', 'Fecha Vencimiento Inspección Técnica V. Tracto',
                           'Fecha Vencimiento Inspección Técnica V. Cisterna', 'N° DGH',
                           'Fecha Vencimiento Resolución MATPEL MTC - TRACTO', 'Nombre Empresa Aseguradora',
                           'Fecha Vencimiento Poliza RC', 'Fecha Vencimiento Poliza Millón Anual',
                           'Fecha Vencimiento Poliza Millón o Poliza RC Pago Mensual', 'Tipologia de Unidades',
                           'Unidad Dedicada a Corporacion Primax', 'Fecha Vencimiento IQBF', 'Nombre Proveedor GPS',
                           'Esta en Plataforma Primax', 'Ultimo Mantenimiento GPS', 'Fecha de Fabricacion de GPS',
                           'Modelo de GPS', 'Lleva Tablet S/N', 'Care Drive S/N (Sensor Fatiga)', 'Camara S/N',
                           'Lanza Neumática S/N', 'Parche Extragrande S/N', 'Cilindro Hermetizador de Manhole S/N',
                           'Globo de Taponamiento S/N', 'Cuenta con Papeleta Multa S/N', 'Barandas de Cisternas',
                           'Escaleras Antideslizante', 'Línea de Vida', 'Código Petro Perú']
        dataFrameTranscord.columns = nombresColumnas

        # Filto de región Lima
        dataFrameTranscord = dataFrameTranscord[dataFrameTranscord['Región'] == 'LIMA']

        # Reiniciar los índices
        dataFrameTranscord = dataFrameTranscord.reset_index(drop=True)

        return dataFrameTranscord

    def organizarDataLTP(self, hojaLTP):
        dataFrameLTP = cargarExcel(self.rutaExcel, hojaLTP, 0)

        # Se seleccionan solo las columnas con datos
        dataFrameLTP = dataFrameLTP.iloc[:, 0:51]

        return dataFrameLTP

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

    def procesarData(self):
        # Organizar data del Excel inicial
        print('Leyendo data de Unidades...')

        # Procesar data Transcord
        self.dataTranscord = self.organizarDataTranscord('Flota Transcord')
        self.guardarIndice(self.dataTranscord, 'transcord')

        # Procesar data LTP
        self.dataLTP = self.organizarDataLTP('Flota LTP')
        self.guardarIndice(self.dataLTP, 'LTP')
