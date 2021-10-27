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
                           'Fecha Vencimiento Póliza Millón o Póliza RC Pago Mensual', 'Tipologia de Unidades',
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
        pass

    def guardarIndice(self, dataFrame, tipo):
        for index, row, in dataFrame.iterrows():
            if tipo == 'transcord':
                placa = row['Placa de Tracto o Camión']
                self.indiceTranscord[placa] = {
                    'Empresa': row['Nombre de Empresa de Transporte'],
                    'Placa Cisterna': row['Placa de Cisterna'],
                    'Propietario': row['Unidad Propia o Tercera'],
                    'Capacidad': row['Capacidad Cisterna'],
                    '# Compartimentos': row['# Compartimentos'],
                    'Compartimentos': [],
                    'Código Petro Perú': row['Código Petro Perú']
                }
                for i in range(1, 10):
                    if pd.notna(row[str(i)]):
                        self.indiceTranscord[placa]['Compartimentos'].append(row[str(i)])
                self.indiceTranscord[placa]['Capacidad'] = self.indiceTranscord[placa]['Capacidad'].replace(' GLS.', '')
                self.indiceTranscord[placa]['Capacidad'] = float(self.indiceTranscord[placa]['Capacidad'])

        with open('archivos_json/transcord.json', 'w', encoding='utf8') as transcordJSON:
            json.dump(self.indiceTranscord, transcordJSON, indent=4, ensure_ascii=False)

    def procesarData(self):
        # Organizar data del Excel inicial
        print('Leyendo data de Unidades...')

        # Procesar data Transcord
        self.dataTranscord = self.organizarDataTranscord('Flota Transcord')
        self.guardarIndice(self.dataTranscord, 'transcord')

        # Procesar data LTP
        self.dataLTP = self.organizarDataLTP('Flota LTP')
        self.guardarIndice(self.dataLTP, 'LTP')
