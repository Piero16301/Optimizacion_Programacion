import pandas as pd

from convertidorLocalizacion import convertirDireccionACoordenadas

if __name__ == "__main__":
    """"
    # Lectura inicial archivo Excel de COESTI
    excelInicial = pd.read_excel('Data_COESTI.xlsx', sheet_name='CL', header=None)
    dataFrameInicial = pd.DataFrame(excelInicial)

    # Se eliminan filas y columnas no necesarias
    filtroFilas = dataFrameInicial.iloc[9:836, 1:37]
    nombresColumnas = ['Centro', 'JOP', 'GOP', 'Transportes', 'Zona', 'Departamento', 'Distrito', 'Estación',
                       'Material', 'Descripción', 'Producto', 'Concatenado', 'Capacidad DGH', 'Inventario Max Deseado',
                       'Muerto', 'Varilla', 'Descarga', 'Stock Operativo', 'VTA Promedio Emergencia', 'X 1', 'X 2',
                       'VTA Promedio %', 'VTA Día 04', 'VTA Día 05', 'Incremento VTA', 'Días Stock Emergencia',
                       'VTA Normal', 'Días Stock Normal', 'Pedido', 'Sugerido', 'Días Stock 1', 'Días Stock 2', 'Y 1',
                       'Cantidad Aproximada Carga', 'Observación', 'Z 1']

    # Asignación de encabezados de todas las columnas
    dataFrameEncabezado = pd.DataFrame(filtroFilas)
    dataFrameEncabezado.columns = nombresColumnas

    # Filtro de filas de zona Lima
    dataFiltroZona = dataFrameEncabezado[dataFrameEncabezado['Zona'] == 'LIMA']

    # Filtro de filas con cantidad sugerida diferente de nulo
    dataFiltroSugerido = dataFiltroZona[dataFiltroZona['Sugerido'].notna()]

    # Reiniciar los índices de las filas
    indicesReiniciados = dataFiltroSugerido.reset_index(drop=True)
    """

    """
    # Guardar como CSV
    indicesReiniciados.to_csv('Data_Formateada.csv', index=False, header=True, sep=',')
    print(indicesReiniciados.to_string())
    """

    # Carga de datos desde CSV
    indicesReiniciados = pd.read_csv('Data_Formateada.csv', sep=',')
    # print(indicesReiniciados.to_string(index=True))

    # Columnas seleccionadas => Centro, Distrito, Estación, Material, Descripción, Producto, Sugerido
    columnasImportantes = indicesReiniciados.iloc[:, [0, 6, 7, 8, 9, 10, 29]]
    print(columnasImportantes.to_string(), "\n")

    # Calculo de la cantidad de G90
    totalG90 = columnasImportantes[columnasImportantes['Producto'] == 'G90']['Sugerido'].sum()
    print('Cantidad G90:', totalG90)

    # Calculo de la cantidad de G95
    totalG95 = columnasImportantes[columnasImportantes['Producto'] == 'G95']['Sugerido'].sum()
    print('Cantidad G95:', totalG95)

    # Calculo de la cantidad de G97
    totalG97 = columnasImportantes[columnasImportantes['Producto'] == 'G97']['Sugerido'].sum()
    print('Cantidad G97:', totalG97)

    # Calculo de la cantidad de Diesel
    totalDiesel = columnasImportantes[columnasImportantes['Producto'] == 'Diesel']['Sugerido'].sum()
    print('Cantidad Diesel:', totalDiesel, '\n')

    # Cantidad total de COESTI
    totalCoesti = totalG90 + totalG95 + totalG97 + totalDiesel
    print('Total COESTI:', totalCoesti)

    # Listas de latitudes y longitudes
    latitudes = []
    longitudes = []

    # Obtención de coordenadas
    for index, row, in columnasImportantes.iterrows():
        direccion = 'Gasolinera Primax ' + row['Estación'] + ' ' + row['Distrito']
        latitud, longitud = convertirDireccionACoordenadas(direccion)
        # print(latitud, longitud)
        latitudes.append(latitud)
        longitudes.append(longitud)

    # Agregar columnas de latitud y longitud al dataframe
    columnasImportantes.insert(7, 'Latitud', latitudes, True)
    columnasImportantes.insert(8, 'Longitud', longitudes, True)

    print(columnasImportantes.to_string())
