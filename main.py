import pandas as pd

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

    # Guardar como CSV
    # indicesReiniciados.to_csv('Data_Formateada.csv', index=True, header=True)
    indicesReiniciados.to_csv('Data_Formateada.csv', index=False, header=True, sep=',')
    print(indicesReiniciados.to_string())
    """

    datosCargados = pd.read_csv('Data_Formateada.csv', sep=',')
    print(datosCargados.to_string(index=True))
