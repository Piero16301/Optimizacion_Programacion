from PreprocesamientoCOESTI import organizarData, guardarExcel, aplicarFiltros, cargarExcel

from ConvertidorLocalizacion import convertirDireccionACoordenadas

if __name__ == "__main__":
    """
    # Organizar data del Excel Inicial
    dataFrameEncabezado = organizarData('Data_COESTI.xlsx')

    # Aplicar filtros
    indicesReiniciados = aplicarFiltros(dataFrameEncabezado)

    # Guardar como Excel
    guardarExcel(indicesReiniciados, 'Data_Formateada.xlsx')
    """

    # Carga de datos desde Excel
    indicesReiniciados = cargarExcel('Data_Formateada.xlsx', 'Sheet1', 0)

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

    # Listas de direcciones, latitudes y longitudes
    direcciones = []
    latitudes = []
    longitudes = []

    # Obtención de coordenadas
    for index, row, in columnasImportantes.iterrows():
        direccion = 'Gasolinera Primax ' + row['Estación'] + ' ' + row['Distrito']
        direccionFormal, latitud, longitud = convertirDireccionACoordenadas(direccion)
        # print(latitud, longitud)
        direcciones.append(direccionFormal)
        latitudes.append(latitud)
        longitudes.append(longitud)

    # Agregar columnas de direccion, latitud y longitud al dataframe
    columnasImportantes.insert(7, 'Dirección', direcciones, True)
    columnasImportantes.insert(8, 'Latitud', latitudes, True)
    columnasImportantes.insert(9, 'Longitud', longitudes, True)

    print(columnasImportantes.to_string())

    # Guardar como Excel
    columnasImportantes.to_excel('Data_Direcciones.xlsx', index=False, header=True)
