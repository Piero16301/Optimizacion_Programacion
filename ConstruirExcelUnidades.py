import json
import pandas as pd


unidadesTranscord = json.load(open('archivos_json/transcord.json', encoding='utf8'))
unidadesLTP = json.load(open('archivos_json/ltp.json', encoding='utf8'))
unidadesApoyo = json.load(open('archivos_json/apoyo.json', encoding='utf8'))

datos = []

encabezados = ['Placa de tracto', 'Flota', 'Empresa', 'Placa de cisterna', 'Propietario', 'Capacidad',
               '# Compartimentos', '1', '2', '3', '4', '5', '6', '7', '8', '9']

for key in unidadesTranscord:
    fila = []

    unidad = unidadesTranscord[key]

    fila.append(key)
    fila.append('TRANSCORD')
    fila.append(unidad['Empresa'])
    fila.append(unidad['Placa Cisterna'])
    fila.append(unidad['Propietario'])
    fila.append(unidad['Capacidad'])
    fila.append(unidad['# Compartimentos'])

    compartimentos = unidad['Compartimentos']

    for i in range(len(compartimentos)):
        fila.append(compartimentos[i])

    datos.append(fila)

for key in unidadesLTP:
    fila = []

    unidad = unidadesLTP[key]

    fila.append(key)
    fila.append('LTP')
    fila.append(unidad['Empresa'])
    fila.append(unidad['Placa Cisterna'])
    fila.append(unidad['Propietario'])
    fila.append(unidad['Capacidad'])
    fila.append(unidad['# Compartimentos'])

    compartimentos = unidad['Compartimentos']

    for i in range(len(compartimentos)):
        fila.append(compartimentos[i])

    datos.append(fila)

for key in unidadesApoyo:
    fila = []

    unidad = unidadesApoyo[key]

    fila.append(key)
    fila.append('APOYO')
    fila.append(unidad['Empresa'])
    fila.append(unidad['Placa Cisterna'])
    fila.append(unidad['Propietario'])
    fila.append(unidad['Capacidad'])
    fila.append(unidad['# Compartimentos'])

    compartimentos = unidad['Compartimentos']

    for i in range(len(compartimentos)):
        fila.append(compartimentos[i])

    datos.append(fila)

dataFrame = pd.DataFrame(datos, columns=encabezados)

print(dataFrame.to_string())

with pd.ExcelWriter('datos_entrada/Detalle_Unidades.xlsx') as archivoExcel:
    dataFrame.to_excel(archivoExcel, index=True, header=True, sheet_name='Hoja 1')

dataFrame = pd.read_excel('datos_entrada/Detalle_Unidades.xlsx', sheet_name='Hoja 1', header=0, index_col=0)

print(dataFrame.to_string())
